// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mtasaStarlightThemePlugin from '@multitheftauto/starlight-theme-mtasa';

// https://astro.build/config
export default defineConfig({
	redirects: {
		"/wiki/[...slug]": "/[...slug]"
	},
	integrations: [
		starlight({
			plugins: [ mtasaStarlightThemePlugin() ],
			title: 'Multi Theft Auto: Wiki',
			logo: {
				replacesTitle: true,
				light: './src/assets/logo-black.png',
				dark: './src/assets/logo-white.png',
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
								{slug: 'Element'},
								{slug: 'Element_tree'},
							]
						},
					]
				},
			],
		}),
	],
});
