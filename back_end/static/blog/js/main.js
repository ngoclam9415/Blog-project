

	'use strict';

  // bootstrap dropdown hover
  
  var get_latest_post_url = window.location.origin + "/get_latest_posts"

  
  verify()
  // loader
  var loader = function() {
    setTimeout(function() { 
      if($('#loader').length > 0) {
        $('#loader').removeClass('show');
      }
    }, 1);
  };
  loader();

  class ViewController{
    constructor(){
      this.latest_posts = [];
      this.favorite_posts = [];
    }
  
    render_latest_post(){
      get_latest_post(get_latest_post_url).then(response => {
        var posts = JSON.parse(response);
        for (let i=0; i<posts.length; i++ ){
          // console.log(posts[i])
          insert_latest_post(posts[i]);
          if (i < 3){
            insert_owl_item(posts[i]);
            insert_popular_posts(posts[i]);
          }
        }
        render_home_slider()
      })
    }
  }
  
  async function get_latest_post(url){
    const response = await fetch(url, {
      method : "POST",
      headers : {
        'Content-Type' : 'application/json'
      },
    })
    return await response.json();
  }
  
  var view_controller = new ViewController();
  view_controller.render_latest_post(get_latest_post_url);

  // Stellar
  $(window).stellar();

	
	$('nav .dropdown').hover(function(){
		var $this = $(this);
		$this.addClass('show');
		$this.find('> a').attr('aria-expanded', true);
		$this.find('.dropdown-menu').addClass('show');
	}, function(){
		var $this = $(this);
			$this.removeClass('show');
			$this.find('> a').attr('aria-expanded', false);
			$this.find('.dropdown-menu').removeClass('show');
	});


	$('#dropdown04').on('show.bs.dropdown', function () {
	  console.log('show');
	});

  // home slider
  function render_home_slider(){
    $('.home-slider').owlCarousel({
      loop:true,
      autoplay: true,
      margin:10,
      animateOut: 'fadeOut',
      animateIn: 'fadeIn',
      nav:true,
      autoplayHoverPause: true,
      items: 1,
      navText : ["<span class='ion-chevron-left'></span>","<span class='ion-chevron-right'></span>"],
      responsive:{
        0:{
          items:1,
          nav:false
        },
        600:{
          items:1,
          nav:false
        },
        1000:{
          items:1,
          nav:true
        }
      }
    });
    
    // owl carousel
    var majorCarousel = $('.js-carousel-1');
    majorCarousel.owlCarousel({
      loop:true,
      autoplay: false,
      stagePadding: 0,
      margin: 10,
      animateOut: 'fadeOut',
      animateIn: 'fadeIn',
      nav: false,
      dots: false,
      autoplayHoverPause: false,
      items: 3,
      responsive:{
        0:{
          items:1,
          nav:false
        },
        600:{
          items:2,
          nav:false
        },
        1000:{
          items:3,
          nav:true,
          loop:false
        }
      }
    });
    
    // cusotm owl navigation events
    $('.custom-next').click(function(event){
      event.preventDefault();
      // majorCarousel.trigger('owl.next');
      majorCarousel.trigger('next.owl.carousel');
    
    })
    $('.custom-prev').click(function(event){
      event.preventDefault();
      // majorCarousel.trigger('owl.prev');
      majorCarousel.trigger('prev.owl.carousel');
    })
    
    // owl carousel
    var major2Carousel = $('.js-carousel-2');
    major2Carousel.owlCarousel({
      loop:true,
      autoplay: true,
      stagePadding: 7,
      margin: 20,
      animateOut: 'fadeOut',
      animateIn: 'fadeIn',
      nav: false,
      autoplayHoverPause: true,
      items: 4,
      navText : ["<span class='ion-chevron-left'></span>","<span class='ion-chevron-right'></span>"],
      responsive:{
        0:{
          items:1,
          nav:false
        },
        600:{
          items:3,
          nav:false
        },
        1000:{
          items:4,
          nav:true,
          loop:false
        }
      }
    });
    
    
    
    
    var contentWayPoint = function() {
      var i = 0;
      $('.element-animate').waypoint( function( direction ) {
    
        if( direction === 'down' && !$(this.element).hasClass('element-animated') ) {
          
          i++;
    
          $(this.element).addClass('item-animate');
          setTimeout(function(){
    
            $('body .element-animate.item-animate').each(function(k){
              var el = $(this);
              setTimeout( function () {
                var effect = el.data('animate-effect');
                if ( effect === 'fadeIn') {
                  el.addClass('fadeIn element-animated');
                } else if ( effect === 'fadeInLeft') {
                  el.addClass('fadeInLeft element-animated');
                } else if ( effect === 'fadeInRight') {
                  el.addClass('fadeInRight element-animated');
                } else {
                  el.addClass('fadeInUp element-animated');
                }
                el.removeClass('item-animate');
              },  k * 100);
            });
            
          }, 100);
          
        }
    
      } , { offset: '95%' } );
    };
    contentWayPoint();

}
	


function verify(){
  var hex_code = window.localStorage.getItem("hex_code");
  if (hex_code !== "0" && hex_code !== undefined && hex_code !== null){
    
    add_newpost_button()
  }
}

function add_newpost_button(){
  $('.col-9.social').append('<a href="/editor"><button type="button" id="new_post" class="btn btn-primary btn-lg">NEW POST</button></a>')
}



function insert_latest_post(data){
  var time = new Date(data.postDate * 1000);
  var new_data = '<div class="col-md-6"><a href=' + window.location.origin+ '/blog/' +data.slug + ' class="blog-entry element-animate fadeIn element-animated" data-animate-effect="fadeIn" style="background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBt8z5qtrx1xSI80zhZ2h1Ba8xg_D06avqRJwNq49hlGXGGu7D"); ">' + '<img src=' + data.thumbnail_IMG_URL +' style="width : 30vw; height : 50vh" alt="Not \n Available">' + 
        '<div class="blog-content-body">' + 
          '<div class="post-meta">' + 
            '<span class="author mr-2"><img src="http://fresherseason2-teamtwo.appspot.com/static/blog/images/person_1.jpg" alt="Colorlib"> Colorlib</span>' +
            '<span class="mr-2">'+ time.toDateString() +' </span> ' + 
            '<span class="ml-2"><span class="fa fa-comments"></span> 3</span>' + 
          '</div>' + 
          '<h2>'+ data.postTitle +'</h2>' + 
        '</div>' + 
      '</a>' + 
    '</div>'
    $("#tableContent").prepend(new_data)
}

function insert_owl_item(data){
  var new_data = '<div>  <a href="blog/blog-single.html" class="a-block d-flex align-items-center height-lg" style="background-image: url(\'blog/images/img_1.jpg\'); ">    <div class="text half-to-full">      <span class="category mb-5">Food</span>      <div class="post-meta">                <span class="author mr-2"><img src="http://fresherseason2-teamtwo.appspot.com/static/blog/images/person_1.jpg" alt="Colorlib"> Colorlib</span>&bullet;        <span class="mr-2">March 15, 2018 </span> &bullet;        <span class="ml-2"><span class="fa fa-comments"></span> 3</span>              </div>      <h3>How to Find the Video Games of Your Youth</h3>    </div>  </a></div>'
  
  var time = new Date(data.postDate*1000);
  new_data = new_data.replace("blog/blog-single.html", window.location.origin+ '/blog/' +data.slug);
  new_data = new_data.replace("blog/images/img_1.jpg", data.thumbnail_IMG_URL);
  new_data = new_data.replace("How to Find the Video Games of Your Youth", data.postTitle);
  new_data = new_data.replace("> Colorlib<", ">" + window.localStorage.getItem("email") + "<");
  new_data = new_data.replace("March 15, 2018", time.toDateString())
  console.log(new_data)
  $(".owl-carousel.owl-theme.home-slider").prepend(new_data);
}

function insert_popular_posts(data){
  var time = new Date(data.postDate*1000);
  var new_data = '<li>  <a href="blog/">    <img src="blog/images/img_2.jpg" alt="Image placeholder" class="mr-4">    <div class="text">      <h4>How to Find the Video Games of Your Youth</h4>      <div class="post-meta">        <span class="mr-2">March 15, 2018 </span>      </div>    </div>  </a></li>'
  new_data = new_data.replace("blog/", window.location.origin+ '/blog/' +data.slug);
  new_data = new_data.replace("March 15, 2018", time.toDateString())
  new_data = new_data.replace('blog/images/img_2.jpg', data.thumbnail_IMG_URL);
  new_data = new_data.replace("How to Find the Video Games of Your Youth", data.postTitle)
  $("#popular_post").find("ul").prepend(new_data);
}