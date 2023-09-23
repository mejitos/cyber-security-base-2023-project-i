"use strict";

import state, { views } from './state.js';
import create_api_client from './api_client.js';
import { clear_node, render_image } from './rendering.js';


(() => {
    const api_client = create_api_client();

    const load_images = async () => {
        try {
            const response = await api_client.get('/api/images');
            return response.data;
        } catch (error) {
            console.log(error);
            return [];
        }
    };

    const load_shared_images = async () => {
        try {
            const response = await api_client.get('/api/images/shared');
            return response.data;
        } catch (error) {
            console.log(error);
            return [];
        }
    };

    const share_image = async (event, image_id) => {
        try {
            await api_client.patch(`/api/images/${image_id}`);

            const share_icon = event.target.querySelector('svg');
            share_icon.classList.toggle('not_shared');

            event.target.title = share_icon.classList.contains('not_shared')
                ? 'Share'
                : 'Unshare';
        } catch (error) {
            console.log(error);
        }
    };

    const remove_image = async (event, image) => {
        try {
            const image_id = image.dataset.imageid;
            await api_client.delete(`/api/images/${image_id}`);

            state.dom.images.removeChild(image);
        } catch (error) {
            console.log(error);
        }
    };

    // Attach event listeners
    document.querySelector('#open_modal')
        .addEventListener('click', event => {
            state.dom.modal.classList.add('open');
        });

    document.querySelector('.modal__backdrop')
        .addEventListener('click', event => {
            state.dom.modal.classList.remove('open');
        });

    document.querySelectorAll('nav button[data-view]')
        .forEach(button => button.addEventListener('click', async event => {
            const new_view = event.target.dataset.view;

            if (state.view === new_view)
                return;

            state.view = new_view;

            const images = new_view === views.SHARED
                ? await load_shared_images()
                : await load_images();

            clear_node(state.dom.images);
            images.forEach(image => render_image(state.dom.images, image));
        }));

    document.querySelector('#upload_form')
        .addEventListener('submit', async event => {
            event.preventDefault();
            const form_data = new FormData(event.target);

            try {
                await api_client.post('/api/images', form_data);
                render_image(state.dom.images, respoonse.data);
            } catch (error) {
                console.log(error);
            }
        });

    document.querySelector('#logout')
        .addEventListener('click', event => {
            event.target.firstElementChild.submit();
        });

    // Load the initial images
    (async () => {
        const images = await load_images();
        clear_node(state.dom.images);
        images.forEach(image => {
            render_image(state.dom.images, image);
        });
    })();
})();
