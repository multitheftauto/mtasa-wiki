import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { glob } from 'astro/loaders';

export const collections = {
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
	elements: defineCollection({
		loader: glob({ pattern: "**/*.yaml", base: "../elements" }),
	}),
};
