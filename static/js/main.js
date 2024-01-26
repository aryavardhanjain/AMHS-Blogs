/*  ---------------------------------------------------
    Template Name: Foodeiblog
    Description:  Foodeiblog Blog HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
    });

    //Search Switch
    $('.search-switch').on('click',function() {
        $('.search-model').fadeIn(400);
    });

    $('.search-close-switch').on('click',function() {
        $('.search-model').fadeOut(400,function() {
            $('#search-input').val('');
        });
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Carousel Slider
    --------------------*/
    var hero_s = $(".hero__slider");
    hero_s.owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='arrow_carrot-left'><span/>", "<span class='arrow_carrot-right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

})(jQuery);

function setBackgroundImages() {
    $('.set-bg').each(function() {
        var bg = $(this).data('setbg')
        $(this).css('background-image', 'url(' + bg + ')')
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    $('#comment-form').submit(function(e) {
        e.preventDefault()
        var formData = $(this).serialize()

        $.ajax({
            type: 'POST',
            url: window.location.href,
            data: formData,
            success: function(response) {
                $('#comment-form')[0].reset()

                var newCommentHtml = `
                    <div class="single-post__comment__item">
                        <div class="single-post__comment__item__text">
                            <h5>${response.comment_name}</h5>
                            <span>${response.comment_date}</span>
                            <p>${response.comment_message}</p>
                            <ul>
                                <li><a href="#"><i class="fa fa-heart-o"></i></a></li>
                            </ul>
                        </div>
                    </div>
                `;
                    
                $('.single-post__comment').append(newCommentHtml);

                var commentCount = parseInt($('#comment-count').text())
                $('#comment-count').text(commentCount + 1)

                if ($('.single-post__comment').children().length > 0){
                    $('.no-comments-message').remove()
                }
            },
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        })
    })
})


document.addEventListener('DOMContentLoaded', function(){
    const loadMoreBtn = document.querySelector('.load__more__btn a')

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href')

            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector('#posts_container').insertAdjacentHTML('beforeend', data.html)
                setBackgroundImages()
                if (data.has_next){
                    loadMoreBtn.setAttribute('href', '?page=' + data.next_page_number)
                } else {
                    loadMoreBtn.style.display = 'none'
                }
            })
            .catch(error => console.error('Error:', error))
        })
    }

    $('.single-post__comment').on('click', '.like-comment', function(e) {
        e.preventDefault()
        const commentId = $(this).data('comment-id')
        const likeIcon = $(this).find('i')

        $.ajax({
            type: 'POST',
            url: `/blogs/like_comment/${commentId}/`,
            data: {
                csrfmiddlewaretoken: csrftoken,
                comment_id: commentId,
            },
            success: function(response) {
                if(response.liked) {
                    likeIcon.removeClass('fa-heart-o').addClass('fa-heart')
                } else {
                    likeIcon.removeClass('fa-heart').addClass('fa-heart-o')
                }
            },
            error: function(response) {
                console.log('Error:', response);
            }
        })
    })
})

document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.nav-link')
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            let url = e.target.dataset.url
            if (url) {
                history.pushState({}, '', url)
            }
        })
    })
})
