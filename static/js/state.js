

export const views = {
    OWN: 'OWN',
    SHARED: 'SHARED',
};

export default {
    dom: {
        modal: document.querySelector('.modal__wrapper'),
        images: document.querySelector('#images'),
    },
    view: views.OWN,
};
