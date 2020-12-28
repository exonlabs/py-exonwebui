<a id="linkmodal_{{id}}" class="text-primary" href="#">{{caption}}</a>
<script type="text/javascript">
  $("#linkmodal_{{id}}").on("click",function(e){
    e.preventDefault();
    WebUI.pagelock.modal(
      '<h5 class="m-0 py-2 text-info"> {{title}}</h5>',
      '{{contents|safe}}',
      '<button class="btn btn-primary" onclick="WebUI.pagelock.hide()">{{gettext("Close")}}</button>',
      '{{styles}}');
    return false;
  });
</script>
