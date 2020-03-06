
/*
Theme Name:       Engage - Bootstrap 4 & HTML5 Template
Author:           UIdeck
Author URI:       http://uideck.com
Text Domain:      UIdeck
Domain Path:      /languages/

JS INDEX
================================================
1. preloader js
2. scroll to top js
3. slick menu js
4. sticky menu js
5. counter js
6. Testimonial owl carousel
7. New Products owl carouse
================================================*/

(function($) {

  var $main_window = $(window);

  /*====================================
  preloader js
  ======================================*/
  $('#preloader').fadeOut();

  /*====================================
  scroll to top js
  ======================================*/
  $main_window.on("scroll", function() {
    if ($(this).scrollTop() > 250) {
      $(".back-to-top").fadeIn(200);
    } else {
      $(".back-to-top").fadeOut(200);
    }
  });
  $(".back-to-top").on("click", function() {
    $("html, body").animate(
      {
        scrollTop: 0
      },
      "slow"
    );
    return false;
  });
    
    

    //===== Sticky
    
    $(window).on('scroll', function(event) {    
        var scroll = $(window).scrollTop();
        if (scroll < 10) {
            $(".navbar-area").removeClass("sticky");
        } else{
            $(".navbar-area").addClass("sticky");
        }
    });
    
    //===== close navbar-collapse when a  clicked
    
    $(".navbar-nav a").on('click', function () {
        $(".navbar-collapse").removeClass("show");
    });
    
    
    //===== Mobile Menu
    
    $(".navbar-toggler").on('click', function(){
        $(this).toggleClass("active");
    });
    
    $(".navbar-nav a").on('click', function() {
        $(".navbar-toggler").removeClass('active');
    });
    
    var subMenu = $(".sub-menu-bar .navbar-nav .sub-menu");
    
    if(subMenu.length) {
        subMenu.parent('li').children('a').append(function () {
            return '<button class="sub-nav-toggler"> <span></span> </button>';
        });
        
        var subMenuToggler = $(".sub-menu-bar .navbar-nav .sub-nav-toggler");
        
        subMenuToggler.on('click', function() {
            $(this).parent().parent().children(".sub-menu").slideToggle();
            return false
        });
        
    }
    
    
    //===== Slick Slider

    function mainSlider() {
        var BasicSlider = $('.header-slider-active');
        BasicSlider.on('init', function (e, slick) {
            var $firstAnimatingElements = $('.single_slider:first-child').find('[data-animation]');
            doAnimations($firstAnimatingElements);
        });
        BasicSlider.on('beforeChange', function (e, slick, currentSlide, nextSlide) {
            var $animatingElements = $('.single_slider[data-slick-index="' + nextSlide + '"]').find('[data-animation]');
            doAnimations($animatingElements);
        });
        BasicSlider.slick({
            autoplay: false,
            autoplaySpeed: 10000,
            dots: true,
            fade: true,
            arrows: true,
            prevArrow: '<span class="prev"></span>',
            nextArrow: '<span class="next"></span>',
            responsive: [
                {
                    breakpoint: 767,
                    settings: {
                        arrows: false
                    }
                }
            ]
        });

        function doAnimations(elements) {
            var animationEndEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
            elements.each(function () {
                var $this = $(this);
                var $animationDelay = $this.data('delay');
                var $animationType = 'animated ' + $this.data('animation');
                $this.css({
                    'animation-delay': $animationDelay,
                    '-webkit-animation-delay': $animationDelay
                });
                $this.addClass($animationType).one(animationEndEvents, function () {
                    $this.removeClass($animationType);
                });
            });
        }
    }
    mainSlider();
    
    

  //WOW Scroll Spy
  var wow = new WOW({
    //disabled for mobile
    mobile: false
  });
  wow.init();

  /* 
  MixitUp
  ========================================================================== */
  $('#portfolio').mixItUp();

  /*=======================================
  counter
  ======================================= */
  if ($(".counter").length > 0) {
    $(".counter").counterUp({
      delay: 1,
      time: 800
    });
  }

  // Progress Bar
  $('.skill-shortcode').appear(function() {
    $('.progress').each(function() {
      $('.progress-bar').css('width', function() {
        return ($(this).attr('data-percentage') + '%')
      });
    });
  }, {
    accY: -100
  });

  /*====================================
  Clients  Owl Carousel
  ======================================*/
  var detailsslider = $("#clients-scroller");
  detailsslider.owlCarousel({
    autoplay: true,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin:30,
    loop: true,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 2,
        },
        991: {
            items: 4,
        }
      }
  });

/*====================================
  New Products Owl Carousel
  ======================================*/
  var newproducts = $("#color-client-scroller");
  newproducts.owlCarousel({
    autoplay: true,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin:5,
    loop: true,
    navText: [
      '<i class="fas fa-angle-left"></i>',
      '<i class="fas fa-angle-right"></i>'
    ],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 3,
        },
        991: {
            items: 4,
        }
      }
  });

/*====================================
  New Products Owl Carousel
  ======================================*/
  var newproducts = $("#testimonial-item");
  newproducts.owlCarousel({
    autoplay: true,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin: 10,
    loop: true,
    navText: [
      '<i class="fas fa-angle-left"></i>',
      '<i class="fas fa-angle-right"></i>'
    ],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 2,
        },
        991: {
            items: 2,
        }
      }
  });


/*====================================
  New Products Owl Carousel
  ======================================*/
  var newproducts = $("#testimonial-dark");
  newproducts.owlCarousel({
    autoplay: true,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin:5,
    loop: true,
    navText: [
      '<i class="fas fa-angle-left"></i>',
      '<i class="fas fa-angle-right"></i>'
    ],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 2,
        },
        991: {
            items: 3,
        }
      }
  });

  /*====================================
  New Products Owl Carousel
  ======================================*/
  var newproducts = $("#single-testimonial-item");
  newproducts.owlCarousel({
    autoplay: true,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin:5,
    loop: true,
    navText: [
      '<i class="fas fa-angle-left"></i>',
      '<i class="fas fa-angle-right"></i>'
    ],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 1,
        },
        991: {
            items: 1,
        }
      }
  });

  /*====================================
  New Products Owl Carousel
  ======================================*/
  var newproducts = $("#image-carousel");
  newproducts.owlCarousel({
    autoplay: true,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin:5,
    loop: true,
    navText: [
      '<i class="fas fa-angle-left"></i>',
      '<i class="fas fa-angle-right"></i>'
    ],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 3,
        },
        991: {
            items: 4,
        }
      }
  });

  /*====================================
  New Products Owl Carousel
  ======================================*/
  var newproducts = $("#carousel-image-slider");
  newproducts.owlCarousel({
    autoplay: false,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin:5,
    loop: true,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 2,
        },
        991: {
            items: 1,
        }
      }
  });

  /*====================================
  New Products Owl Carousel
  ======================================*/
  var newproducts = $("#carousel-about-us");
  newproducts.owlCarousel({
    autoplay: true,
    nav: false,
    autoplayHoverPause:true,
    smartSpeed: 350,
    dots: true,
    margin:5,
    loop: true,
    navText: [
      '<i class="fas fa-angle-left"></i>',
      '<i class="fas fa-angle-right"></i>'
    ],
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        575: {
            items: 1,
        },
        991: {
            items: 1,
        }
      }
      
  });



})(jQuery);

