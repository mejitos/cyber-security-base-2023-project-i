

const create_api_client = (options = {}) => {
    const BASE_URL = options.base_url || '';

    const get = async (resource) => {
        const response = await fetch(`${BASE_URL}${resource}`, {
            method: 'GET',
        });
        const data = await response.json();

        return {
            data,
        };
    };

    const post = async (resource, body) => {
        const response = await fetch(`${BASE_URL}${resource}`, {
            method: 'POST',
            body,
        });
        const data = await response.json();

        return {
            data,
        };
    };

    const patch = async (resource) => {
        const response = await fetch(`${BASE_URL}${resource}`, {
            method: 'PATCH',
        });
        const data = await response.json();

        return {
            data,
        };
    };

    const _delete = async (resource) => {
        const response = await fetch(`${BASE_URL}${resource}`, {
            method: 'DELETE',
        });
        const data = await response.json();

        return {
            data,
        };
    };

    return {
        get,
        post,
        patch,
        delete: _delete,
    };
};

export default create_api_client;
