// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mtasaStarlightThemePlugin from '@multitheftauto/starlight-theme-mtasa';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			plugins: [ mtasaStarlightThemePlugin() ],
			title: 'Multi Theft Auto: Wiki',
			sidebar: [
				{
					slug: 'introduction',
				},
				{
					label: 'Lua API Reference',
					items: [
						{slug: 'Client_Scripting_Functions'},
						{slug: 'Client_Scripting_Events'},
						{slug: 'Server_Scripting_Functions'},
						{slug: 'Server_Scripting_Events'},
						{slug: 'Shared_Scripting_Functions'},
						// {slug: 'Useful_Functions'},
						{slug: 'Element'},
						{slug: 'Element_tree'},
					]
				},
			],
		}),
	],
});
