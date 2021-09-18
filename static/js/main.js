$(function() {

  "use strict";
  /***************************

  swup

  ***************************/
  const options = {
    containers: ['#dynamic-content'],
    animateHistoryBrowsing: true,
    linkSelector: '.trm-menu a:not([data-no-swup]), .trm-anima-link:not([data-no-swup])',
    animationSelector: '[class="dynamic-content"]'
  };
  const swup = new Swup(options);
});
