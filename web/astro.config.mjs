// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mtasaStarlightThemePlugin from '@multitheftauto/starlight-theme-mtasa';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			plugins: [
				mtasaStarlightThemePlugin(),
			],
			favicon: 'favicon.ico',
			title: 'Multi Theft Auto: Wiki',
			logo: {
				replacesTitle: true,
				light: './src/assets/logo-black.png',
				dark: './src/assets/logo-white.png',
			},
			components: {
				// Override some default components
				Pagination: './src/overrides/Pagination.astro',
			},
			disable404Route: true,
			sidebar: [
				{
					label: 'Start here',
					items: [
						{
							label: 'Introduction', link: 'Introduction',
						},
					]
				},
				{
					label: 'Reference',
					items: [
						{
							label: 'Lua API', link: 'Lua_API',
						},
						{
							label: 'Functions',
							items: [
								{label: 'All functions', link: 'Scripting_Functions'},
								{label: 'Shared functions', link: 'Shared_Scripting_Functions'},
								{label: 'Client functions', link: 'Client_Scripting_Functions'},
								{label: 'Server functions', link: 'Server_Scripting_Functions'},
							]
						},
						{
							label: 'Events',
							items: [
								{label: 'All events', link: 'Scripting_Events'},
								{label: 'Client events', link: 'Client_Scripting_Events'},
								{label: 'Server events', link: 'Server_Scripting_Events'},
							]
						},
						{
							label: 'Elements',
							items: [
								{label: 'Element types', link: 'Element', badge:{
									text: 'New',
									variant: 'tip',
								}},
								{label: 'Element tree', link: 'Element_tree'},
							]
						},
					]
				},
			],
		}),
	],
});
