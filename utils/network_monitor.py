"""
Network monitoring and diagnostics utilities
"""

import time
import threading
import psutil
import requests
import socket
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import deque
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class NetworkMetrics:
    """Network performance metrics"""
    timestamp: datetime
    download_speed: float  # Mbps
    upload_speed: float    # Mbps
    latency: float         # ms
    packet_loss: float     # percentage
    jitter: float          # ms
    connection_quality: str # excellent, good, fair, poor
    bandwidth_usage: float # percentage

class NetworkMonitor:
    """Comprehensive network monitoring and diagnostics"""
    
    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self.metrics_history = deque(maxlen=history_size)
        self.is_monitoring = False
        self.monitor_thread = None
        self.last_net_io = psutil.net_io_counters()
        self.last_net_io_time = time.time()
        
        # Test servers for different regions
        self.test_servers = {
            'global': [
                'https://www.cloudflare.com/cdn-cgi/trace',
                'https://httpbin.org/ip',
                'https://api.ipify.org'
            ],
            'speed_test': [
                'https://speed.cloudflare.com/__down',
                'https://speed.cloudflare.com/__up'
            ],
            'dns_test': [
                '1.1.1.1',  # Cloudflare
                '8.8.8.8',  # Google
                '208.67.222.222'  # OpenDNS
            ]
        }
    
    def start_monitoring(self, interval: int = 30):
        """Start continuous network monitoring"""
        if self.is_monitoring:
            logger.warning("Network monitoring already running")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        logger.info(f"Network monitoring started with {interval}s interval")
    
    def stop_monitoring(self):
        """Stop network monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Network monitoring stopped")
    
    def _monitor_loop(self, interval: int):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                metrics = self.get_current_metrics()
                self.metrics_history.append(metrics)
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def get_current_metrics(self) -> NetworkMetrics:
        """Get current network metrics"""
        # Get bandwidth usage
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        
        time_diff = current_time - self.last_net_io_time
        bytes_sent = current_net_io.bytes_sent - self.last_net_io.bytes_sent
        bytes_recv = current_net_io.bytes_recv - self.last_net_io.bytes_recv
        
        # Convert to Mbps
        download_speed = (bytes_recv * 8) / (time_diff * 1_000_000)  # Mbps
        upload_speed = (bytes_sent * 8) / (time_diff * 1_000_000)    # Mbps
        
        # Update last values
        self.last_net_io = current_net_io
        self.last_net_io_time = current_time
        
        # Get latency and packet loss
        latency, packet_loss = self._measure_latency()
        
        # Calculate jitter
        jitter = self._calculate_jitter()
        
        # Determine connection quality
        connection_quality = self._assess_connection_quality(
            latency, packet_loss, download_speed
        )
        
        # Calculate bandwidth usage percentage
        bandwidth_usage = self._calculate_bandwidth_usage(download_speed, upload_speed)
        
        return NetworkMetrics(
            timestamp=datetime.now(),
            download_speed=download_speed,
            upload_speed=upload_speed,
            latency=latency,
            packet_loss=packet_loss,
            jitter=jitter,
            connection_quality=connection_quality,
            bandwidth_usage=bandwidth_usage
        )
    
    def _measure_latency(self) -> Tuple[float, float]:
        """Measure latency and packet loss to multiple servers"""
        latencies = []
        successful_pings = 0
        total_pings = 0
        
        for server in self.test_servers['dns_test']:
            try:
                # Use ping command for accurate measurement
                if hasattr(subprocess, 'run'):
                    result = subprocess.run(
                        ['ping', '-c', '3', '-W', '1000', server],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        # Parse ping output for latency
                        lines = result.stdout.split('\n')
                        for line in lines:
                            if 'time=' in line:
                                time_str = line.split('time=')[1].split()[0]
                                try:
                                    latency = float(time_str)
                                    latencies.append(latency)
                                    successful_pings += 1
                                except ValueError:
                                    pass
                        total_pings += 3
                else:
                    # Fallback to socket-based measurement
                    start_time = time.time()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((server, 53))
                    sock.close()
                    
                    if result == 0:
                        latency = (time.time() - start_time) * 1000
                        latencies.append(latency)
                        successful_pings += 1
                    total_pings += 1
                    
            except Exception as e:
                logger.debug(f"Failed to ping {server}: {e}")
                total_pings += 3
        
        if not latencies:
            return 999.0, 100.0  # High latency, 100% packet loss
        
        avg_latency = sum(latencies) / len(latencies)
        packet_loss = ((total_pings - successful_pings) / total_pings) * 100
        
        return avg_latency, packet_loss
    
    def _calculate_jitter(self) -> float:
        """Calculate jitter from recent latency measurements"""
        if len(self.metrics_history) < 2:
            return 0.0
        
        recent_latencies = [
            metrics.latency for metrics in list(self.metrics_history)[-10:]
        ]
        
        if len(recent_latencies) < 2:
            return 0.0
        
        # Calculate jitter as the average difference between consecutive latencies
        differences = []
        for i in range(1, len(recent_latencies)):
            differences.append(abs(recent_latencies[i] - recent_latencies[i-1]))
        
        return sum(differences) / len(differences) if differences else 0.0
    
    def _assess_connection_quality(self, latency: float, packet_loss: float, 
                                 download_speed: float) -> str:
        """Assess overall connection quality"""
        score = 0
        
        # Latency scoring (lower is better)
        if latency < 20:
            score += 3
        elif latency < 50:
            score += 2
        elif latency < 100:
            score += 1
        
        # Packet loss scoring (lower is better)
        if packet_loss < 1:
            score += 3
        elif packet_loss < 5:
            score += 2
        elif packet_loss < 10:
            score += 1
        
        # Speed scoring (higher is better)
        if download_speed > 100:
            score += 3
        elif download_speed > 50:
            score += 2
        elif download_speed > 10:
            score += 1
        
        # Determine quality based on total score
        if score >= 8:
            return "excellent"
        elif score >= 6:
            return "good"
        elif score >= 4:
            return "fair"
        else:
            return "poor"
    
    def _calculate_bandwidth_usage(self, download_speed: float, 
                                 upload_speed: float) -> float:
        """Calculate bandwidth usage percentage"""
        # Assume a typical home connection of 100 Mbps
        total_bandwidth = 100.0
        total_usage = download_speed + upload_speed
        return min((total_usage / total_bandwidth) * 100, 100.0)
    
    def get_network_info(self) -> Dict:
        """Get comprehensive network information"""
        try:
            # Get network interfaces
            interfaces = []
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {
                    'name': interface,
                    'addresses': [],
                    'stats': None
                }
                
                for addr in addrs:
                    interface_info['addresses'].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                
                # Get interface statistics
                try:
                    stats = psutil.net_if_stats()[interface]
                    interface_info['stats'] = {
                        'isup': stats.isup,
                        'duplex': stats.duplex,
                        'speed': stats.speed,
                        'mtu': stats.mtu
                    }
                except KeyError:
                    pass
                
                interfaces.append(interface_info)
            
            # Get current metrics
            current_metrics = self.get_current_metrics()
            
            # Get external IP and location
            external_ip = self._get_external_ip()
            location_info = self._get_location_info(external_ip)
            
            return {
                'interfaces': interfaces,
                'current_metrics': {
                    'download_speed': current_metrics.download_speed,
                    'upload_speed': current_metrics.upload_speed,
                    'latency': current_metrics.latency,
                    'packet_loss': current_metrics.packet_loss,
                    'jitter': current_metrics.jitter,
                    'connection_quality': current_metrics.connection_quality,
                    'bandwidth_usage': current_metrics.bandwidth_usage,
                    'timestamp': current_metrics.timestamp.isoformat()
                },
                'external_ip': external_ip,
                'location': location_info,
                'history': [
                    {
                        'timestamp': m.timestamp.isoformat(),
                        'download_speed': m.download_speed,
                        'upload_speed': m.upload_speed,
                        'latency': m.latency,
                        'packet_loss': m.packet_loss,
                        'connection_quality': m.connection_quality
                    }
                    for m in list(self.metrics_history)[-20:]  # Last 20 measurements
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {'error': str(e)}
    
    def _get_external_ip(self) -> Optional[str]:
        """Get external IP address"""
        for url in self.test_servers['global']:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    if 'ipify' in url:
                        return response.text.strip()
                    elif 'httpbin' in url:
                        data = response.json()
                        return data.get('origin', '').split(',')[0]
                    elif 'cloudflare' in url:
                        # Parse Cloudflare trace response
                        lines = response.text.split('\n')
                        for line in lines:
                            if line.startswith('ip='):
                                return line.split('=')[1]
            except Exception as e:
                logger.debug(f"Failed to get IP from {url}: {e}")
                continue
        
        return None
    
    def _get_location_info(self, ip: Optional[str]) -> Dict:
        """Get location information for IP address"""
        if not ip:
            return {}
        
        try:
            # Use ipapi.co for location info
            response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country_name'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'timezone': data.get('timezone'),
                    'isp': data.get('org')
                }
        except Exception as e:
            logger.debug(f"Failed to get location info: {e}")
        
        return {}
    
    def run_speed_test(self) -> Dict:
        """Run a comprehensive speed test"""
        results = {
            'download_speed': 0.0,
            'upload_speed': 0.0,
            'latency': 0.0,
            'timestamp': datetime.now().isoformat(),
            'status': 'failed'
        }
        
        try:
            # Test download speed
            download_speeds = []
            for _ in range(3):
                start_time = time.time()
                response = requests.get(
                    'https://speed.cloudflare.com/__down?bytes=25000000',  # 25MB
                    timeout=30,
                    stream=True
                )
                
                if response.status_code == 200:
                    bytes_downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        bytes_downloaded += len(chunk)
                    
                    duration = time.time() - start_time
                    speed = (bytes_downloaded * 8) / (duration * 1_000_000)  # Mbps
                    download_speeds.append(speed)
            
            if download_speeds:
                results['download_speed'] = sum(download_speeds) / len(download_speeds)
            
            # Test upload speed (simplified)
            upload_speeds = []
            test_data = b'0' * 10_000_000  # 10MB
            
            for _ in range(3):
                start_time = time.time()
                response = requests.post(
                    'https://httpbin.org/post',
                    data=test_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    duration = time.time() - start_time
                    speed = (len(test_data) * 8) / (duration * 1_000_000)  # Mbps
                    upload_speeds.append(speed)
            
            if upload_speeds:
                results['upload_speed'] = sum(upload_speeds) / len(upload_speeds)
            
            # Test latency
            latency, _ = self._measure_latency()
            results['latency'] = latency
            
            results['status'] = 'success'
            
        except Exception as e:
            logger.error(f"Speed test failed: {e}")
            results['error'] = str(e)
        
        return results
    
    def get_network_health_report(self) -> Dict:
        """Generate a comprehensive network health report"""
        current_metrics = self.get_current_metrics()
        
        # Analyze historical data
        if len(self.metrics_history) > 0:
            recent_metrics = list(self.metrics_history)[-10:]
            avg_latency = sum(m.latency for m in recent_metrics) / len(recent_metrics)
            avg_packet_loss = sum(m.packet_loss for m in recent_metrics) / len(recent_metrics)
            avg_download = sum(m.download_speed for m in recent_metrics) / len(recent_metrics)
        else:
            avg_latency = current_metrics.latency
            avg_packet_loss = current_metrics.packet_loss
            avg_download = current_metrics.download_speed
        
        # Generate recommendations
        recommendations = []
        
        if current_metrics.latency > 100:
            recommendations.append("High latency detected. Check your internet connection and consider using a closer server.")
        
        if current_metrics.packet_loss > 5:
            recommendations.append("High packet loss detected. This may indicate network congestion or hardware issues.")
        
        if current_metrics.download_speed < 10:
            recommendations.append("Low download speed. Check if other applications are using bandwidth.")
        
        if current_metrics.connection_quality == "poor":
            recommendations.append("Connection quality is poor. Consider restarting your router or contacting your ISP.")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'current_status': {
                'connection_quality': current_metrics.connection_quality,
                'download_speed': current_metrics.download_speed,
                'upload_speed': current_metrics.upload_speed,
                'latency': current_metrics.latency,
                'packet_loss': current_metrics.packet_loss,
                'jitter': current_metrics.jitter,
                'bandwidth_usage': current_metrics.bandwidth_usage
            },
            'averages': {
                'latency': avg_latency,
                'packet_loss': avg_packet_loss,
                'download_speed': avg_download
            },
            'recommendations': recommendations,
            'overall_health': 'good' if current_metrics.connection_quality in ['excellent', 'good'] else 'needs_attention'
        }

# Global network monitor instance
network_monitor = NetworkMonitor() 