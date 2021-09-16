window.onload = function () {
    bulmaCarousel.attach("#carousel", {
        slidesToScroll: 1,
        slidesToShow: 4,
        loop: true,
        autoplay: false,
        breakpoints: [{
            changePoint: 480,
            slidesToShow: 1,
            slidesToScroll: 1
        }, {
            changePoint: 640,
            slidesToShow: 2,
            slidesToScroll: 1
        }, {
            changePoint: 768,
            slidesToShow: 3,
            slidesToScroll: 1
        }]
    })
};