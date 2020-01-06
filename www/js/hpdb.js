allowLoggedinlocalhost = true;
localsid = 'a3c8a198e3133f4a83fc0ab382a37ee20d9496360edcc0f9f65274cca8bcd0f6';

var comboTreeObj;

function getsid() {
  sid = localStorage.getItem('sid');
  if (sid == null) sid = sessionStorage.getItem('sid');
  return sid;
}

function fileTree(sid) {
  $('#fileTree').fileTree({
    root: '',
    multiSelect: true,
    script: '/cgi-bin/jqueryFileTree.cgi?sid=' + sid
  }, function(file) {
    $('#' + inputFileID ).val(file);
    $('#fileTree_modal').modal('hide');
  });
  $('#fileTree2').fileTree({
    root: '',
    script: '/cgi-bin/jqueryFileTree.cgi?sid=' + sid
  }, function(file) {});
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
  $('.tool_form').append('<input type="hidden" name="sid" value="' + sid + '">');
  $('#gen_comp_anal_form').append('<input type="hidden" name="sid" value="' + sid + '">');
  $('#importdb_form').append('<input type="hidden" name="sid" value="' + sid + '">');
  $('#username_label').text('Hi, ' + username);
  $('#export_table').attr("href", '/cgi-bin/export_html.cgi?sid=' + sid);
  fileTree(sid);
  $("#uploader").pluploadQueue({
    runtimes: 'html5,flash,silverlight,html4',
    url: '/upload.php?sid=' + getsid(),
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

function load_pubmed_data() {
  var eutilSearchURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?usehistory=y&db=pubmed&term=Helicobacter%20pylori&retmode=json';
  
  $.getJSON(eutilSearchURL, function(pubmedList) {
    if (pubmedList.esearchresult.count > 0) {
      var pmids = pubmedList.esearchresult.idlist;
      var retmax = 5;
      var eutilSummaryURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=' + pmids + '&retmax=' + retmax + '&retmode=json';
      var ulItem = [];
      ulItem.push('<ul>');
      
      $.getJSON(eutilSummaryURL, function(pubmedSummary) {
        for (var i = 0; i < pubmedSummary.result.uids.length; i++) {
          var value = pubmedSummary.result.uids[i];
          var author;
          if (pubmedSummary.result[value].authors.length == 1) {
            author = pubmedSummary.result[value].authors[0].name;
          } else if (pubmedSummary.result[value].authors.length == 2) {
            author = pubmedSummary.result[value].authors[0].name + ' and ' + pubmedSummary.result[value].authors[1].name;
          } else {
            author = pubmedSummary.result[value].authors[0].name + ' et al.';
          }
          
          var listItem = [];
          listItem.push('<li>');
          listItem.push('<div>' + pubmedSummary.result[value].pubdate + '</div>');
          listItem.push('<a href="https://www.ncbi.nlm.nih.gov/pubmed/' +  value + '" target="_blank">' + pubmedSummary.result[value].title + '</a>');
          listItem.push('<div>' + author + '</div>');
          listItem.push('<div>' + pubmedSummary.result[value].source + '</div>');
          listItem.push('</li>');
          ulItem.push(listItem.join('\n'));
        }
        // add show more link
        ulItem.push('<a href="https://www.ncbi.nlm.nih.gov/pubmed/?term=Helicobacter%20pylori" target="_blank">show more >></a>');
        ulItem.push('</ul>');
        $('#pubmed').html(ulItem.join('\n'));
      });
    } else {
      $('#pubmed').html('<ul><li>No recent articles found.</li></ul>');
    }
  });
}

function load_strains_list() {
  let dropdown = $('#strains_list');
  dropdown.empty();

  $.getJSON('/cgi-bin/list_strains.cgi', function (data) {
    $.each(data, function (key, entry) {
      dropdown.append($('<option></option>').attr('value', entry.ncbi_id).text(entry.name));
    })
  });

  $.getJSON('/cgi-bin/list_database.cgi', function (data) {
    comboTreeObj = $('#import_combo_tree').comboTree({
			source : data,
			isMultiple: true,
			cascadeSelect: true,
			collapse: true
		});
  });
}

function delete_job(link) {
  $.get({
    url: link,
    success: function(responseText, statusText, xhr) {
      alert(responseText);
      //$('#projects_btn').click();
    }
  });
}

function submit_import() {
  $.post({
    url: '/cgi-bin/user_importdb.cgi',
    data: {
      sid: getsid(),
      ids: JSON.stringify(comboTreeObj.getSelectedIds())
    },
    success: function(responseText, statusText, xhr) {
      alert(responseText);
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
      $('#vf_align_result').text(responseText);
    }
  });
  $('.tool_form').ajaxForm({
    clearForm: true,
    beforeSubmit: function(arr, $form, options) {
      $form.find(':submit').text('Submitting...');
      $form.find(':submit').attr('disabled', 'disabled');
      $form.find(':submit').removeClass('btn-primary').addClass('btn-secondary');
      $form.find(':submit').hide().show(0); // hack to force redrawing button
    },
    error: function(xhr, status, error, $form) {
      alert(error.responseText);
      $form.find(':submit').text('Submit');
      $form.find(':submit').removeAttr('disabled');
      $form.find(':submit').removeClass('btn-secondary').addClass('btn-primary');
    },
    success: function(responseText, statusText, xhr, $form) {
      alert(responseText);
      $form.find(':submit').text('Submit');
      $form.find(':submit').removeAttr('disabled');
      $form.find(':submit').removeClass('btn-secondary').addClass('btn-primary');
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
      url: '/cgi-bin/user_getjobs.cgi',
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
  load_strains_list();
  load_pubmed_data();
  checkSession();
});