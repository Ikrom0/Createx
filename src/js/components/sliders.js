import Swiper from 'swiper'
import 'swiper/css'
import 'swiper/css/grid'
import { Navigation, Pagination, Autoplay, Thumbs, Grid } from 'swiper/modules'

export default function initSliders() {

  initIntroSlider()
  initProjectSlider()
  initReviewSlider()
  initGallerySlider()
  initHistorySlider()
  initPartnerSlider()
  initFactSlider()
  initPlanSlider()

}

function initIntroSlider() {
  const slider = document.querySelector('#intro-slider')
  if (!slider) return

  new Swiper(slider, {
    modules: [Navigation, Pagination, Autoplay],
    loop: true,
    autoplay: window.innerWidth > 768
    ? {
        delay: 3000,
      }
    : false,
    speed: 800,

    navigation: {
      nextEl: '.intro .slider-btn--next',
      prevEl: '.intro .slider-btn--prev'
    },

    pagination: {
      el: '.intro__pagination',
      clickable: true,
      renderBullet: (index, className) => `
        <span class="${className}">
          <span class="intro__bullet-number">${String(index + 1).padStart(2, '0')}</span>
          <span class="intro__bullet-fill"></span>
        </span>`
    },

    on: {
      autoplayTimeLeft(swiper, time, progress) {
        const fills = document.querySelectorAll('.intro__bullet-fill')
        const active = fills[swiper.realIndex]
        if (active) active.style.transform = `scaleX(${1 - progress})`
      },

      slideChange() {
        document.querySelectorAll('.intro__bullet-fill')
          .forEach(el => el.style.transform = 'scaleX(0)')
      }
    }
  })
}

function initProjectSlider() {
  const slider = document.querySelector('#projects-slider')
  
  if (!slider) return

  new Swiper(slider, {
    modules: [Navigation, Pagination],
    speed: 500,
    spaceBetween: 30,
    loop: true,

    pagination: {
      el: slider.querySelector('.swiper-pagination'),
      clickable: true,
    },

    breakpoints: {
      993: {
        slidesPerView: 3
      },

      576: {
        slidesPerView: 2
      }
    },

    navigation: {
      nextEl: '.projects .slider-btn--next',
      prevEl: '.projects .slider-btn--prev'
    }
  })
}

function initReviewSlider() {
  const slider = document.querySelector('#review-slider')
  const container = document.querySelector('.review__content')

  if (!slider) return

  new Swiper(slider, {
    modules: [Navigation, Pagination],
    speed: 500,
    loop: true,

    pagination: {
      el: container.querySelector('.swiper-pagination'),
      clickable: true,
    },

    navigation: {
      nextEl: '.review .slider-btn--next',
      prevEl: '.review .slider-btn--prev'
    }
  })
}

function initGallerySlider() {
  const gallery = document.querySelector('#gallery-slider')
  const thumbs = document.querySelector('#gallery-thumbs')

  if (!gallery || !thumbs) return

  const thumbsSwiper = new Swiper(thumbs, {
    slidesPerView: 'auto',
    spaceBetween: 10,
    watchSlidesProgress: true,
    slideToClickedSlide: true
  })

  new Swiper(gallery, {
    modules: [Navigation, Thumbs],
    speed: 1000,
    loop: true,

    navigation: {
      prevEl: '.gallery .slider-btn--prev',
      nextEl: '.gallery .slider-btn--next'
    },

    thumbs: {
      swiper: thumbsSwiper
    }
  })
}

function initHistorySlider() {
  const slider = document.querySelector('#history-slider')

  if (!slider) return

  const historySwiper = new Swiper(slider, {
    modules: [Navigation],
    spaceBetween: 30,
    speed: 800,
    loop: true,

    navigation: {
      nextEl: '.history .slider-btn--next',
      prevEl: '.history .slider-btn--prev'
    }
  })

  const historyThumbs = document.querySelectorAll('.history__thumbs-item')

  historyThumbs.forEach((item, i) => {
    item.onclick = () => historySwiper.slideToLoop(i)
  })

  historySwiper.on('slideChange', () => {
    const { realIndex } = historySwiper

    historyThumbs.forEach((el, i) => {
      el.classList.remove('history__thumbs-item--active')
      el.removeAttribute('aria-current')

      if (i === realIndex) {
        el.classList.add('history__thumbs-item--active')
        el.setAttribute('aria-current', 'true')
      }
    })
  })
}

function initPartnerSlider() {
  const slider = document.querySelector('#partners-slider');
  const slider2 = document.querySelector('#partners-about-slider');
  
  const partnerSliderOptions = {
    modules: [Autoplay, Grid],
    loop: true,
    speed: 500,
    slidesPerView: 2,
    spaceBetween: 40,

    autoplay: {
      delay: 1500,
      pauseOnMouseEnter: true,
    },

    breakpoints: {
      1200: {
        slidesPerView: 6,
      },
      992: {
        slidesPerView: 5,
      },
      768: {
        slidesPerView: 4,
      },
      576: {
        slidesPerView: 3,
      },
    },
  };

  if (slider2) {
    new Swiper(slider2, {
      ...partnerSliderOptions,
      grid: {
        rows: 2,
        fill: 'row',
      },
    });
  }

  if (slider) {
    new Swiper(slider, partnerSliderOptions);
  }
}

function initPlanSlider() {
  const slider = document.querySelector('#plan-slider')

  if (!slider) return

  new Swiper(slider, {
    modules: [Pagination],
    spaceBetween: 30,

    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    
    breakpoints: {
      992: {
        slidesPerView: 4,
      },

      768: {
        slidesPerView: 3,
      },

      576: {
        slidesPerView: 2,
      }
    }
  })
}

function initFactSlider() {
  const slider = document.querySelector('#facts-slider')

  if (!slider) return

  new Swiper(slider, {
    modules: [Autoplay],
    loop: true,
    speed: 500,
    autoplay: {
      delay: 1500,
      pauseOnMouseEnter: true,
    },

    breakpoints: {
      992: {
        slidesPerView: 4,
      },

      768: {
        slidesPerView: 3,
      },

      576: {
        slidesPerView: 2,
      }
    }
  })
}
