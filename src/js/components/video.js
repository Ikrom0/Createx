export default function initVideo() {
  
  const btn = document.querySelector('.video__btn')
  
  if (btn) {
    btn.addEventListener('click', () => {
    
      const video = document.querySelector('.video__media')
      const videoWrapper = document.querySelector('.video__wrapper')
  
      if (video.readyState >= 2) {
        videoWrapper.classList.add('video__wrapper--active')
      } else {
        video.addEventListener('loadeddata', () => {
          videoWrapper.classList.add('video__wrapper--active')
        }, { once: true })
      }
    
      video.play()
    })
  }

}



