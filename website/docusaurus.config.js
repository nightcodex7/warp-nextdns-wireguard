// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const {themes} = require('prism-react-renderer');
const lightTheme = themes.github;
const darkTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'WARP NextDNS Manager',
  tagline: 'Secure your connection with Cloudflare WARP and NextDNS',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://nightcodex7.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/warp-nextdns-wireguard/',

  // GitHub pages deployment config.
  organizationName: 'nightcodex7', // Usually your GitHub org/user name.
  projectName: 'warp-nextdns-wireguard', // Usually your repo name.
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
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
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/nightcodex7/warp-nextdns-wireguard/tree/testing/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
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
        title: 'WARP NextDNS Manager',
        logo: {
          alt: 'WARP NextDNS Logo',
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
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Installation',
                to: '/docs/installation',
              },
              {
                label: 'Getting Started',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/nightcodex7/warp-nextdns-wireguard',
              },
              {
                label: 'Issues',
                href: 'https://github.com/nightcodex7/warp-nextdns-wireguard/issues',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Releases',
                href: 'https://github.com/nightcodex7/warp-nextdns-wireguard/releases',
              },
              {
                label: 'Changelog',
                href: 'https://github.com/nightcodex7/warp-nextdns-wireguard/blob/main/CHANGELOG.md',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} WARP NextDNS Manager. Built with Docusaurus.`,
      },
      prism: {
        theme: lightTheme,
        darkTheme: darkTheme,
        additionalLanguages: ['bash', 'python'],
      },
    }),
};

module.exports = config;