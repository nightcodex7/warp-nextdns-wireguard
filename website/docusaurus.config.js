// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'WARP + NextDNS Manager',
  tagline: 'Enterprise-Grade Cloudflare WARP + NextDNS Integration',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://nightcodex7.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/warp-nextdns-wireguard/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'nightcodex7', // Usually your GitHub org/user name.
  projectName: 'warp-nextdns-wireguard', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/nightcodex7/warp-nextdns-wireguard/tree/main/website/',
        },
        blog: false, // Disable blog
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'WARP + NextDNS Manager',
        logo: {
          alt: 'WARP + NextDNS Manager Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {
            href: 'https://github.com/nightcodex7/warp-nextdns-wireguard',
            label: 'GitHub',
            position: 'right',
          },
          {
            href: 'https://github.com/nightcodex7/warp-nextdns-wireguard/discussions',
            label: 'Discussions',
            position: 'right',
          },
          {
            href: 'https://buymeacoffee.com/nightcode',
            label: '☕ Buy Me a Coffee',
            position: 'right',
            className: 'donation-link',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/intro',
              },
              {
                label: 'Installation',
                to: '/docs/installation',
              },
              {
                label: 'Configuration',
                to: '/docs/configuration',
              },
              {
                label: 'API Reference',
                to: '/docs/api',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub Discussions',
                href: 'https://github.com/nightcodex7/warp-nextdns-wireguard/discussions',
              },
              {
                label: 'GitHub Issues',
                href: 'https://github.com/nightcodex7/warp-nextdns-wireguard/issues',
              },
              {
                label: 'Contributing',
                to: '/docs/contributing',
              },
            ],
          },
          {
            title: 'Support',
            items: [
              {
                label: '☕ Buy Me a Coffee',
                href: 'https://buymeacoffee.com/nightcode',
              },
              {
                label: '💙 Support on Ko-fi',
                href: 'https://ko-fi.com/nightcode',
              },
              {
                label: 'Security Policy',
                to: '/docs/security',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} WARP + NextDNS Manager. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
      colorMode: {
        defaultMode: 'system',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
    }),

  // Add custom CSS for donation links
  customCss: [
    require.resolve('./src/css/custom.css'),
  ],
};

module.exports = config; 