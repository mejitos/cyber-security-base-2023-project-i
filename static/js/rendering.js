import state, { views } from './state.js';
import api_client from './api_client.js';


export const clear_node = (node) => {
    while (node.firstChild)
        node.removeChild(node.firstChild);
};

export const render_image = (parent, image) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'glass image__wrapper';
    wrapper.dataset.imageid = image.id;

    const img = document.createElement('img');
    // TODO: Add username
    img.src = `/static/images/${image.filename}`;
    img.alt = image.title;

    const text = document.createElement('div');
    text.className = 'image__text';

    const title = document.createElement('h3');
    title.appendChild(document.createTextNode(image.title));
    text.appendChild(title);

    const description = document.createElement('p');
    description.appendChild(document.createTextNode(image.description));
    text.appendChild(description);

    if (state.view === views.SHARED) {
        const author = document.createElement('span');
        const by = `by ${image.owner}`;
        author.appendChild(document.createTextNode(by));
        text.appendChild(author);
    } else {
        const actions = document.createElement('div');
        text.appendChild(actions);

        const remove = document.createElement('button');
        remove.title = 'Remove';
        const remove_icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        remove_icon.setAttributeNS(null, 'viewBox', '0 0 24 24');
        const remove_path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        remove_path.setAttributeNS(null, 'd', 'M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z');
        remove_icon.appendChild(remove_path);
        remove.appendChild(remove_icon);
        remove.addEventListener('click', async event => {
            try {
                const image_id = wrapper.dataset.imageid;
                await api_client.delete(`/api/images/${image_id}`);

                state.dom.images.removeChild(wrapper);
            } catch (error) {
                console.log(error);
            }
        });
        actions.appendChild(remove);

        const share = document.createElement('button');
        share.title = image.shared ? 'Unshare' : 'Share';
        const share_icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        share_icon.setAttributeNS(null, 'class', image.shared ? '' : 'not_shared');
        share_icon.setAttributeNS(null, 'viewBox', '0 0 24 24');
        const share_path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        share_path.setAttributeNS(null, 'd', 'M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z');
        share_icon.appendChild(share_path)
        share.appendChild(share_icon);
        share.addEventListener('click', async event => {
            try {
                await api_client.patch(`/api/images/${image.id}`);

                const share_icon = event.target.querySelector('svg');
                share_icon.classList.toggle('not_shared');

                event.target.title = share_icon.classList.contains('not_shared')
                    ? 'Share'
                    : 'Unshare';
            } catch (error) {
                console.log(error);
            }
        });
        actions.appendChild(share);
    }

    wrapper.appendChild(img);
    wrapper.appendChild(text)
    parent.appendChild(wrapper);
};
