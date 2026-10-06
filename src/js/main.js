import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import '@styles/main.scss';

import 'simplebar';
import 'simplebar/dist/simplebar.min.css';

import initGalleryLightbox from './components/lightbox';
import initModals from './components/modal'
import initAccordion from './components/accordion'
import initVideo from './components/video'
import initNews from './components/news';
import initPortfolio from './components/work';
import initHeader from './components/header';
import initSliders from './components/sliders'
import initInputMask from './components/input-mask';
import initSidebar from './components/sidebar';
import setupForm from './components/form';


document.addEventListener('DOMContentLoaded', () => {

  initModals()
  initAccordion()
  initVideo()
  initSliders()
  initHeader()
  initGalleryLightbox()
  initInputMask()
  initSidebar()
  
  setupForm("[data-request-form]")
  setupForm("[data-application-form]", "modal")
  setupForm("[data-subscribe-form]", "modal")
  setupForm("[data-comment-form]", "comment")
  setupForm("[data-project-form]")
  setupForm("[data-article-form]")
  setupForm("[data-login-form]")

  if (document.querySelector('.news')) { initNews() }
  if (document.querySelector('.projects--work')) { initPortfolio() }

});


