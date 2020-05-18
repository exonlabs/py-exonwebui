/*
  :copyright: 2020, ExonLabs. All rights reserved.
  :license: BSD, see LICENSE for more details.
*/
var WebUI = function($, ui) {

  ui.board_content = {
    old_hash: null,
    load_neglect: false,
    update: function(data) {
      $("#board-content").html(data);
    },
    error: function(message) {
      ui.board_content.update(
        '<div class="p-3"><div class="alert alert-danger text-left">' +
        '<i class="fas fa-ta fa-exclamation-circle"></i> ' + message + '</div></div>');
    },
    warn: function(message) {
      ui.board_content.update(
        '<div class="p-3"><div class="alert alert-warning text-left">' +
        '<i class="fas fa-ta fa-exclamation-circle"></i> ' + message + '</div></div>');
    },
    info: function(message) {
      ui.board_content.update(
        '<div class="p-3"><div class="alert alert-info text-left">' +
        '<i class="fas fa-ta fa-info-circle"></i> ' + message + '</div></div>');
    },
    success: function(message) {
      ui.board_content.update(
        '<div class="p-3"><div class="alert alert-success text-left">' +
        '<i class="fas fa-ta fa-check-circle"></i> ' + message + '</div></div>');
    },
    load: function(url, params) {
      if(ui.board_content.load_neglect) {
        ui.board_content.load_neglect = false;
        return null;
      };
      ui.loader.load("GET", url, params,
        function(result) {
          ui.board_content.old_hash = window.location.hash;
          if(result.redirect) ui.redirect(result.redirect, result.blank);
          else {
            if(result.doctitle) ui.doctitle.update(result.doctitle);
            if(result.notifications) ui.notify.load(result.notifications);
            if(result.payload !== undefined) ui.board_content.update(result.payload);
          };
        },
        function(error) {
          ui.notify.error(error);
          if(ui.board_content.old_hash) {
            ui.board_content.load_neglect = true;
            window.location.hash = ui.board_content.old_hash;
          };
        });
    }
  };

  ui.board_init = function() {
    ui.init();

    $(window)
      .bind("hashchange", function(e) {
        e.preventDefault();
        ui.board_content.load(window.location.hash, null);
      });

    $('#menubar-body a.pagelink[href="' +
        window.location.hash.replace(/[\/?].*$/,"") + '"]')
      .parents('ul').prev('a').click();

    $("body")
      .on("click", "a.pagelink", function(e) {
        e.preventDefault();
        ui.redirect($(this).attr("href"));
      });

    if(window.location.hash.length <= 1) {
      window.location.hash = $('#menubar-body a.pagelink').attr("href");
    }
    else $(window).trigger("hashchange");
  };

  return ui;
}(jQuery, WebUI || {});
