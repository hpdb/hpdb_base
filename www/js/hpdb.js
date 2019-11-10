allowLoggedinlocalhost = true;
localsid = 'a3c8a198e3133f4a83fc0ab382a37ee20d9496360edcc0f9f65274cca8bcd0f6';

function getsid() {
  sid = localStorage.getItem('sid');
  if (sid == null) sid = sessionStorage.getItem('sid');
  return sid;
}

function fileTree(sid) {
  $('#fileTree').fileTree({
    root: '',
    script: 'http://hpdb.tk/cgi-bin/jqueryFileTree.cgi?sid=' + sid
  }, function(file) {
    $('#' + inputFileID ).val(file);
    $('#fileTree_modal').modal('hide');
  });
}

function signup(input) {
  $.ajax({
    type: 'POST',
    url: '/cgi-bin/user_management.cgi',
    dataType: 'json',
    cache: false,
    data: $.param({'action': 'signup',
                   'email': input.email,
                   'username': input.username,
                   'hash': sha256(input.password)}),
    error: function() {
      alert('Failed to sign up. Please check server error log for detail.');
      location.reload(true);
    },
    success: function(data) {
      if (data.success == true) {
        alert('Success');
      } else {
        alert('Failed');
      }
      location.reload(true);
    }
  });
}

function login(input) {
  var timestamp = Date.now().toString();
  var hashed_pass = sha256(input.password);
  $.ajax({
    type: 'POST',
    url: '/cgi-bin/user_management.cgi',
    dataType: 'json',
    cache: false,
    data: $.param({'action': 'login',
                   'username': input.username,
                   'hash': sha256(timestamp + hashed_pass),
                   'timestamp': timestamp}),
    error: function() {
      console.log('Failed to login in. Please check server error log for detail.');
      $('#login_username').addClass('is-invalid');
      $('#login_password').addClass('is-invalid');
      $('#login_invalid_help').show();
    },
    success: function(data) {
      if (data.success == true) { // login success
        if (input.remember)
          localStorage.setItem('sid', data.sid);
        else
          sessionStorage.setItem('sid', data.sid);
        location.reload(true);
      }  else {
        $('#login_username').addClass('is-invalid');
        $('#login_password').addClass('is-invalid');
        $('#login_invalid_help').show();
      }
    }
  });
}

function logout(sid) {
  $.ajax({
    type: 'POST',
    url: '/cgi-bin/user_management.cgi',
    dataType: 'json',
    cache: false,
    data: $.param({'action': 'logout', 'sid': sid})
  });
}

function showLoggedin(sid, username) {
  $('#logout_btn').show();
  $('.loggedin-item').show();
  $('.loggedout-item').hide();
  $('#username_label').text('Hi, ' + username);
  $('#hpdb_form').append('<input type="hidden" name="sid" value="' + sid + '">');
  $('#roary_form').append('<input type="hidden" name="sid" value="' + sid + '">');
  $('#vf_align_form').append('<input type="hidden" name="sid" value="' + sid + '">');
  fileTree(sid);
  $("#uploader").pluploadQueue({
    runtimes: 'html5,flash,silverlight,html4',
    url: 'http://hpdb.tk/upload.php?sid=' + getsid(),
    chunk_size: '1mb',
    rename: true,
    sortable: true,
    dragdrop: true,

    filters: {
      // Maximum file size
      max_file_size: '1gb',
      // Specify what files to browse for
      mime_types: [
        {title: "text/plain", extensions: "fastq,fq,fa,fasta,fna,contigs,gbk,genbank,gb,txt,text,config,ini,xls,xlsx"},
        {title: "application/x-gzip", extensions: "gz"}
      ]
    },

    flash_swf_url: 'js/plupload/Moxie.swf',
    silverlight_xap_url: 'js/plupload/Moxie.xap'
  });
}

function showLoggedout() {
  $('#login_btn').show();
  $('.loggedout-item').show();
  $('.loggedin-item').hide();
}

function checkSession() {
  if (allowLoggedinlocalhost && (location.hostname === 'localhost' || location.hostname === '127.0.0.1')) {
    console.log('Running on local server. Skipped checkSession!');
    localStorage.setItem('sid', localsid);
    showLoggedin(localsid, 'baohiep');
    return;
  }
  sid = getsid();
  if (sid == null) {
    showLoggedout();
    return;
  }
  $.ajax({
    type: 'POST',
    url: '/cgi-bin/user_management.cgi',
    dataType: 'json',
    cache: false,
    data: $.param({'action': 'check', 'sid': sid}),
    error: function() {
      console.log('Failed to login. Please check server error log for detail.');
    },
    success: function(data) {
      if (data.success == true) {
        showLoggedin(sid, data.username);
      }  else {
        localStorage.removeItem('sid');
        location.reload(true);
      }
    }
  });
}

$(document).ready(function () {
  /* SIDEBAR */
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar').toggleClass('active');
  });
  $('#sidebar .nav-link').on('click', function() {
    $('#sidebar .nav-link').not(this).removeClass('active');
    if ($(window).width() <= 768) {
      $('#sidebar').removeClass('active');
    }
  });

  $('#sidebar > ul > li > a').on('click', function() {
    $('.submenu').collapse('hide');
  });

  /* Comment out to enable swipe gestures
  $('#sidebar').on('swipeleft', function() {
    $('#sidebar').removeClass('active');
  });
  $('#content').on('swiperight', function() {
    $('#sidebar').addClass('active');
  }); */

  /* SCROLL TO TOP */
  $('#content').on('scroll', function() {
    100 < $(this).scrollTop() ? $('.scroll-to-top').fadeIn() : $('.scroll-to-top').fadeOut()
  });
  $('.scroll-to-top').on('click', function(e) {
    $('#content').animate({scrollTop : 0}, 700);
    e.preventDefault()
  });

  $('.custom-file-input').on('change', function() {
    let files = $(this)[0].files;
    let val = (files.length > 1) ? (files.length + ' files selected') : $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass('selected').html(val);
  });

  /* FORM */
  $('#vf_align_form').ajaxForm({
    beforeSubmit: function() {
      $('#vf_align_result').text('Submitting... Please wait...');
    },
    error: function(error) {
      $('#vf_align_result').text(error.responseText);
    },
    success: function(responseText) {
      $('#vf_align_result').text(responseText)
    }
  });

  /* Make all links open in new tabs */
  $(document.links).filter(function() {
    return this.hostname != window.location.hostname || this.href.includes('cgi-bin');
  }).attr('target', '_blank');

  /* Enable all tooltips */
  $('[data-toggle="tooltip"]').tooltip();

  $('#login_submit').on('click', function(e){
    e.preventDefault();
    var data = {
      username: $('#login_username').val().replace(/ /g, ''),
      password: $('#login_password').val(),
      remember: $('#rememberme').is(':checked')
    }
    if (data.username.length == 0) {
      $('#login_invalid_help').hide();
      $('#login_username').addClass('is-invalid');
      $('#login_username_help').show();
    } else {
      $('#login_username').removeClass('is-invalid');
      $('#login_username_help').hide();
    }
    if (data.password.length == 0) {
      $('#login_invalid_help').hide();
      $('#login_password').addClass('is-invalid');
      $('#login_password_help').show();
    } else {
      $('#login_password').removeClass('is-invalid');
      $('#login_password_help').hide();
    }
    if (data.username && data.password) {
      $('#login_invalid_help').hide();
      login(data);
    }
  });

  $('#logout_btn').on('click', function(e) {
    e.preventDefault();
    if (localStorage.getItem('sid') != null) {
      logout(localStorage.getItem('sid'));
      localStorage.removeItem('sid');
    }
    if (sessionStorage.getItem('sid') != null) {
      logout(sessionStorage.getItem('sid'));
      sessionStorage.removeItem('sid');
    }
    location.reload(true);
  });

  $('#signup_submit').on('click', function(e) {
    e.preventDefault();
    var data = {
      email: $('#signup_email').val().replace(/ /g, ''),
      username: $('#signup_username').val().replace(/ /g, ''),
      password: $('#signup_password').val()
    }
    if (data.email.length == 0) {
      $('#signup_email').addClass('is-invalid');
      $('#signup_email_help').show();
    } else {
      $('#signup_email').removeClass('is-invalid');
      $('#signup_email_help').hide();
    }
    if (data.username.length == 0) {
      $('#signup_username').addClass('is-invalid');
      $('#signup_username_help').show();
    } else {
      $('#signup_username').removeClass('is-invalid');
      $('#signup_username_help').hide();
    }
    if (data.password.length == 0) {
      $('#signup_password').addClass('is-invalid');
      $('#signup_password_help').show();
    } else {
      $('#signup_password').removeClass('is-invalid');
      $('#signup_password_help').hide();
    }
    if (data.email && data.username && data.password) {
      signup(data);
    }
  });

  $('#login_username, #login_password').keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();
        $("#login_submit").trigger('click');
    }
  });

  $('#projects_btn').on('click', function(e) {
    $("#p_status").hide();
    $("#search_ptable").hide();
    $('#projects_table').hide();
    sid = getsid();
    if (sid == null) {
      $("#p_status").text("You are not logged in!");
      $("#p_status").show();
      return;
    }
    $('#p_spinner').removeClass('d-none');
    $.ajax({
      type: 'POST',
      url: 'http://hpdb.tk/cgi-bin/user_getjobs.cgi',
      cache: false,
      data: $.param({'sid': getsid()}), // FIX-ME: Check when sid is null
      success: function(data) {
        $('#p_spinner').addClass('d-none');
        if (data.length < 10) {
          $("#p_status").text("You haven't submitted any projects!");
          $("#p_status").show();
        } else {
          $('#projects_table tbody').html(data);
          $("#search_ptable").trigger('keyup');
          $("#p_status").text("You have submitted " + ($('#projects_table tr').length - 1) + ' project(s).');
          $("#p_status").show();
          $("#search_ptable").show();
          $('#projects_table').show();
        }
      },
      error: function() {
        $('#p_spinner').addClass('d-none');
        $("#p_status").text("Server error! Please contact admin.");
        $("#p_status").show();
      }
    });
  });

  $('#search_ptable').on('keyup', function() {
    var value = $(this).val().toLowerCase();
    $('#projects_table tr').each(function() {
      td = $(this).find('td:first');
      $(this).toggle(td.text().toLowerCase().indexOf(value) > -1)
    });
  });

  $('form').on('submit', function() {
    //$(this).trigger("reset");
  });

  $('.file-selector').on('click', function() {
    inputFileID = $(this).parent().prev('input').attr('id');
  });

  checkSession();
});