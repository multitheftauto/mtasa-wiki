import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { glob } from 'astro/loaders';

export const collections = {
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
	elements: defineCollection({
		loader: glob({
			pattern: "**/*.yaml",
			base: "../elements",
			generateId: ({ entry }) => entry.replace(/\.yaml$/, '')
		}),
	}),
	functions: defineCollection({
		loader: glob({
			pattern: "**/*.yaml",
			base: "../functions",
			generateId: ({ entry }) => {
				// Extract the file name without the folder
				return ((entry.split('/') || []).pop() || '').replace(/\.yaml$/, '');
			}
		})
	}),
};
