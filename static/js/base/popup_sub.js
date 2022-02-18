const cover = $(".cover");
const popup = $('[data-popup-sub=""]');
const popup_trigger = $('[data-popup-sub-trigger=""]')

cover.each( (index, cover) => {
    $(cover).on('click', e => {
        $(cover).addClass('hidden');
        popup.addClass('hidden');
    });
})

popup_trigger.on('click', e => {
    cover.removeClass('hidden');
    popup.removeClass('hidden');
})