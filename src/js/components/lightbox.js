import lightGallery from 'lightgallery'
import lgZoom from 'lightgallery/plugins/zoom'

import 'lightgallery/css/lightgallery.css'
import 'lightgallery/css/lg-zoom.css'

function initGalleryLightbox() {
  const gallery = document.querySelector('#gallery-slider')

  if (!gallery) return;

  lightGallery(gallery, {
    selector: '.gallery__item',
    plugins: [lgZoom],
    download: false,

    mobileSettings: {
      controls: true,
      showCloseIcon: true,
    },
  })
}

export default initGalleryLightbox