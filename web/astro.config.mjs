// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mtasaStarlightThemePlugin from '@multitheftauto/starlight-theme-mtasa';
import starlightLinksValidator from 'starlight-links-validator'

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			plugins: [
				mtasaStarlightThemePlugin(),
				starlightLinksValidator(),
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
							slug: 'introduction',
						},
					]
				},
				{
					label: 'Reference',
					items: [
						{
							slug: 'lua-api',
						},
						{
							label: 'Functions',
							items: [
								{label: 'All functions', link: '/functions'},
								{label: 'Shared functions', link: 'Shared_Scripting_Functions'},
								{label: 'Client functions', link: 'Client_Scripting_Functions'},
								{label: 'Server functions', link: 'Server_Scripting_Functions'},
							]
						},
						{
							label: 'Events',
							items: [
								// {slug: 'Client_Scripting_Events'},
								// {slug: 'Server_Scripting_Events'},
							]
						},
						{
							label: 'Elements',
							items: [
								{label: 'Element types', link: '/Element', badge:{
									text: 'New',
									variant: 'tip',
								}},
								{slug: 'Element_tree'},
							]
						},
					]
				},
			],
		}),
	],
});
