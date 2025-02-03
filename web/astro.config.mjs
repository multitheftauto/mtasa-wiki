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
							slug: 'Lua_API',
						},
						{
							label: 'Functions',
							items: [
								{slug: 'Client_Scripting_Functions'},
								{slug: 'Server_Scripting_Functions'},
								{slug: 'Shared_Scripting_Functions'},
							]
						},
						{
							label: 'Events',
							items: [
								{slug: 'Client_Scripting_Events'},
								{slug: 'Server_Scripting_Events'},
							]
						},
						{
							label: 'Elements',
							items: [
								{label: 'Element types', link: '/Element'},
								{slug: 'Element_tree'},
							]
						},
					]
				},
			],
		}),
	],
});
