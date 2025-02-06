import type { APIRoute } from 'astro';

const CFRedirects = `
/wiki/ /
/wiki/* /:splat
`;

export const GET: APIRoute = () => {
    return new Response(CFRedirects);
};
