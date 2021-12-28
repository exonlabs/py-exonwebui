<script type="text/javascript">
  $(document).ready(function(){
    $("{{container|safe}}").on("click","{{selector|safe}}",function(e){
      e.preventDefault();
      WebUI.loader.load("POST", $(this).attr("href"), null,
        function(result){
          if(result.redirect) WebUI.redirect(result.redirect,result.blank);
          else {
            if(result.notifications) WebUI.notify.load(result.notifications);
            if(result.contents) WebUI.pagelock.modal(
              result.title, result.contents,
              result.footer?result.footer:'<button class="btn btn-primary" onclick="WebUI.pagelock.hide()">{{gettext("Close")}}</button>',
              '{{styles}}');
          };
        });
      return false;
    });
  });
</script>
