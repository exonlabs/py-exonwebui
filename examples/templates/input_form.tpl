<div class="container-fluid pt-3 pb-5">
  <div class="row">
    <div class="col-xs-12 col-md-10">
      <div class="card">
        <div class="card-header">
          {{gettext('Input Form Title')}}
        </div>
        <div id="InputForm" class="card-body">
          {{contents|safe}}
        </div>
        <div class="card-footer text-right">
          <button id="btn_reset" class="btn btn-sm btn-secondary mx-1">{{gettext('Reset')}}</button>
          <button id="btn_submit" class="btn btn-sm btn-primary mx-1">{{gettext('Submit')}}</button>
        </div>
      </div>
    </div>
  </div>
</div>
<script type="text/javascript">
  $(document).ready(function() {
    $("#btn_submit").on("click", function(){$("#InputForm form").trigger('submit')});
    $("#btn_reset").on("click", function(){$("#InputForm form").trigger('reset')});
  });
</script>
