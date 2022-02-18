const theme_toggler = $("#theme_toggle");

const theme_choice = localStorage.getItem('theme_choice');

theme_choice === null
    ? localStorage.setItem('theme_choice', 'dark')
    : null;

theme_choice === 'light'
    ? theme_toggler.prop('checked', true)
    : theme_toggler.prop('checked', false);

theme_toggler.on('click', e => {
    theme_toggler.prop('checked')
        ? localStorage.setItem('theme_choice', 'light')
        : localStorage.setItem('theme_choice', 'dark');
})