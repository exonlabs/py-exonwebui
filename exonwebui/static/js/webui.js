/*
  :copyright: 2020, ExonLabs. All rights reserved.
  :license: BSD, see LICENSE for more details.
*/
var WebUI = function($, ui) {

  ui.format_url = function(url) {
    return "/" + url.replace(/^[\/#]/, "");
  };

  ui.doctitle = {
    base: document.title,
    update: function(title) {
      if(title !== undefined && title.length > 0) {
        title = title[0].toUpperCase() + title.slice(1);
        document.title = title + " | " + ui.doctitle.base;
      };
    },
    reset: function() {
      document.title = ui.doctitle.base;
    }
  };

  ui.pagelock = {
    show: function(html, styles) {
      ui.pagelock.hide();
      $("body").append('<div id="_UiPageLock" class="container-fluid overflow-auto scroll page-lock '+(styles?styles:'')+'">'+(html?html:'')+'</div>');
    },
    loading: function(html) {
      ui.pagelock.show('<div class="row"><div class="col cancel"><a id="_UiPageLock_btnCancel"><i class="fas fa-times"></i></a></div></div>'+(html?html:''),'page-loading');
      $("#_UiPageLock_btnCancel").on('click',function(){ui.pagelock.hide()});
      return $("#_UiPageLock_btnCancel");
    },
    progress: function(percent) {
      if(percent) $("#_UiPageLock .progress-bar").css("width", percent+"%");
      else return ui.pagelock.loading('<div class="row h-100 align-items-center justify-content-center"><div class="col-5"><div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated"></div></div></div></div>');
    },
    modal: function(title, contents, footer, styles) {
      ui.pagelock.show('<div class="modal-dialog modal-dialog-centered '+(styles?styles:'')+'"><div class="modal-content"><div class="modal-header pt-2 pb-1">'+(title?title:'')+'<button class="close" onclick="WebUI.pagelock.hide()">×</button></div><div class="modal-body scroll">'+(contents?contents:'')+(footer?'</div><div class="modal-footer p-1">'+footer+'</div></div></div>':''));
    },
    hide: function() {
      if($("#_UiPageLock").length) $("#_UiPageLock").remove();
    }
  };

  ui.notify = {
    stack: {"dir1":"down", "dir2":"left", "push":"top",
            "firstpos1":14, "firstpos2":10, "spacing1":7, "spacing2":7},
    clear: PNotify.removeAll,
    show: function(category, message, unique, sticky) {
      if(unique) PNotify.removeAll();
      if(window.innerWidth < 576) {
        ui.notify.stack.firstpos1 = 0; ui.notify.stack.firstpos2 = 0;
      } else {
        ui.notify.stack.firstpos1 = 14; ui.notify.stack.firstpos2 = 10;
      };
      if($("html").attr("dir") == "rtl" || $("body").attr("dir") == "rtl")
        ui.notify.stack.dir2 = "right";
      else ui.notify.stack.dir2 = "left";
      var opt = {
        styling: "fontawesome", icon: false, hide: (sticky?false:true),
        animate_speed: "fast", buttons: {sticker:false, closer:true},
        addclass: "stack-custom", stack: ui.notify.stack
      };
      if(category == "error") {
        opt.type = "error";
        opt.text = '<i class="fas fa-ta fa-exclamation-circle"></i> ' + message;
      } else if(category == "warn") {
        opt.type = "notice";
        opt.text = '<i class="fas fa-ta fa-exclamation-circle"></i> ' + message;
      } else if(category == "success") {
        opt.type = "success";
        opt.text = '<i class="fas fa-ta fa-check-circle"></i> ' + message;
      } else {
        opt.type = "info";
        opt.text = '<i class="fas fa-ta fa-info-circle"></i> ' + message;
      };
      var n = new PNotify(opt);
      n.get().click(function() {n.remove()});
    },
    error: function(message, unique, sticky) {
      ui.notify.show('error', message, unique, sticky);
    },
    warn: function(message, unique, sticky) {
      ui.notify.show('warn', message, unique, sticky);
    },
    info: function(message, unique, sticky) {
      ui.notify.show('info', message, unique, sticky);
    },
    success: function(message, unique, sticky) {
      ui.notify.show('success', message, unique, sticky);
    },
    load: function(notifications) {
      for(var i=0; i<notifications.length; i++)
        ui.notify.show(notifications[i][0],notifications[i][1],notifications[i][2],notifications[i][3]);
    }
  };

  ui.scrolltop = function(interval) {
    $("body").animate({scrollTop:0},(interval)?interval:300);
  };

  ui.redirect = function(url, blank) {
    if(url !== undefined && url.length > 0) {
      if(url[0] == '#') {
        if(url == window.location.hash) $(window).trigger("hashchange");
        else window.location.hash = url;
      }
      else if(blank) window.open(url);
      else if(url == window.location) location.reload();
      else window.location = url;
    };
  };

  ui.request = function(verb, url, params, fSuccess, fError, fComplete) {
    return $.ajax({
      url: ui.format_url(url), type: verb, data: params?params:{},
      success: function(result, status, xhr) {
        if(typeof fSuccess === "function") fSuccess(result);
        else {
          if(result.notifications) ui.notify.load(result.notifications);
          if(result.redirect) ui.redirect(result.redirect, result.blank);
        };
      },
      error: function(xhr, status, error) {
        if(error == 'abort') error = "request cancelled";
        else if(!xhr.status) error = "service unavailable";
        else if(!error) error = "request failed";
        if(typeof fError === "function") fError($.i18n._(error));
        else ui.notify.error($.i18n._(error));
      },
      complete: function(xhr, status) {
        if(typeof fComplete === "function") fComplete();
      }
    });
  };

  ui.loader = {
    req_xhr: null,
    lock_timer: null,
    progress_timer: null,
    progress_xhr: null,
    load: function(verb, url, params, fSuccess, fError, fComplete, timeout) {
      ui.loader.cancel();
      ui.loader.lock_timer = setTimeout(function() {
        ui.pagelock.loading().off("click").on("click", function(e) {ui.loader.cancel()});
      }, (timeout)?timeout:500);
      ui.loader.req_xhr = ui.request(verb, url, params, fSuccess, fError,
        function() {
          ui.loader.reset();
          ui.pagelock.hide();
          if(typeof fComplete === "function") fComplete();
        }
      );
    },
    progress: function(verb, url, params, fSuccess, fError, fComplete, timeout, interval) {
      ui.loader.cancel();
      ui.loader.lock_timer = setTimeout(function() {
        ui.pagelock.progress().off("click").on("click", function(e) {ui.loader.cancel()});
        ui.loader.progress_timer = setInterval(function() {
          if(ui.loader.progress_xhr === null) {
            ui.loader.progress_xhr = ui.request(verb, url, {_csrf_token:Cookies.get("_csrf_token"),get_progress:1},
              function(r){ui.pagelock.progress(r.payload)}, function(e){}, function(){ui.loader.progress_xhr=null});
          };
        }, (interval)?interval:5000);
      }, (timeout)?timeout:500);
      ui.loader.req_xhr = ui.request(verb, url, params, fSuccess, fError,
        function() {
          ui.loader.reset();
          ui.pagelock.progress(100);
          setTimeout(function() {
            ui.pagelock.hide();
            if(typeof fComplete === "function") fComplete();
          }, 400);
        }
      );
    },
    cancel: function() {
      if(ui.loader.req_xhr) ui.loader.req_xhr.abort();
    },
    reset: function() {
      if(ui.loader.lock_timer) clearTimeout(ui.loader.lock_timer);
      if(ui.loader.progress_timer) clearTimeout(ui.loader.progress_timer);
      ui.loader.req_xhr = null;
      ui.loader.lock_timer = null;
      ui.loader.progress_timer = null;
    }
  };

  ui.init = function() {
    var lang = $('html').attr("lang");
    if(lang && typeof(webui_i18n) != "undefined") {
      $.i18n.load(webui_i18n, lang);
    };
  };

  return ui;
}(jQuery, WebUI || {});
