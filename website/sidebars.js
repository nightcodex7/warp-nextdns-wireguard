/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'installation',
        'quick-start',
        'prerequisites',
      ],
    },
    {
      type: 'category',
      label: 'User Guide',
      items: [
        'configuration',
        'web-interface',
        'cli-interface',
        'gui-interface',
        'features',
      ],
    },
    {
      type: 'category',
      label: 'Advanced',
      items: [
        'advanced-configuration',
        'network-diagnostics',
        'security',
        'backup-restore',
        'troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'Development',
      items: [
        'api',
        'development',
        'contributing',
        'testing',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
        'cli-reference',
        'configuration-reference',
        'faq',
        'changelog',
      ],
    },
  ],
};

module.exports = sidebars; 