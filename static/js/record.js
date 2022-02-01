// coloring card! win -> royalblue, lose -> crimson

const cards = document.querySelectorAll('.card');

[...cards].forEach(card => {
    if (card.dataset.result == 'True') {
        card.classList.add('card-win');
    } else {
        card.classList.add('card-lose');
    }
})

// tooltip initial

$(function () {
    $(".tooltip-div").tooltip();
});