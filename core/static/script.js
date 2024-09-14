document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.carousel .item');
    const thumbnails = document.querySelectorAll('.thumb li');
    let currentIndex = 0;
    let autoSlideInterval;

    function changeSlide(index) {
        items.forEach((item, idx) => {
            item.classList.remove('active');
            thumbnails[idx].classList.remove('active');
        });
        items[index].classList.add('active');
        thumbnails[index].classList.add('active');
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % items.length;
        changeSlide(currentIndex);
    }
    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', () => {
            clearInterval(autoSlideInterval);
            currentIndex = index;
            changeSlide(currentIndex);
            autoSlideInterval = setInterval(nextSlide, 5000);
        });
    });

    autoSlideInterval = setInterval(nextSlide, 5000);
    changeSlide(currentIndex);
});