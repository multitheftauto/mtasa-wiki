import { getCollection } from 'astro:content';
import path from 'path';

type FunctionItem = Awaited<ReturnType<typeof getCollection>>[number];

type FunctionsByCategory = {
    [folder: string]: FunctionItem[];
};
type FunctionsByTypeByCategory = {
    shared: FunctionsByCategory;
    client: FunctionsByCategory;
    server: FunctionsByCategory;
};

export type FunctionData = {
    shared?: any;
    client?: any;
    server?: any;
};

function getFunctionType(data: FunctionData): 'shared' | 'client' | 'server' {
    if (data.shared) return 'shared';
    if (data.client) return 'client';
    return 'server';
}
function getFunctionTypePretty(data: FunctionData): string {
    const funcType = getFunctionType(data);
    if (funcType === 'shared') return 'Shared';
    if (funcType === 'client') return 'Client-side';
    return 'Server-side';
}

export function getFunctionInfo(data: FunctionData): any {
    return {
        description: data.shared?.description || data.client?.description || data.server?.description || '',
        type: getFunctionType(data),
        typePretty: getFunctionTypePretty(data),
        pair: data.shared?.pair || data.client?.pair || data.server?.pair || false,
    };
}

const functionsCollection = await getCollection('functions');
let functionsByCategory: FunctionsByCategory = {};
let functionsByTypeByCategory: FunctionsByTypeByCategory = {
    shared: {},
    client: {},
    server: {}
};

for (let func of functionsCollection) {
    const normalizedPath = path.normalize(func.filePath || '');
    const folder = path.basename(path.dirname(normalizedPath));
    if (!functionsByCategory[folder]) {
        functionsByCategory[folder] = [];
    }
    functionsByCategory[folder].push(func);

    const funcType = getFunctionType(func.data);
    if (!functionsByTypeByCategory[funcType][folder]) {
        functionsByTypeByCategory[funcType][folder] = [];
    }
    functionsByTypeByCategory[funcType][folder].push(func);
}

export function getFunctionsByCategory(): FunctionsByCategory {
    return functionsByCategory;
}

export function getFunctionsByTypeByCategory(): FunctionsByTypeByCategory {
    return functionsByTypeByCategory;
}