<form id="frmLogin_{{id}}">
  <div class="form-group mb-2">
    <label class="control-label font-weight-bold mb-1 float-left">{{gettext("Username")}}</label>
    <input type="text" class="form-control" name="username" value="">
  </div>
  <div class="form-group">
    <label class="control-label font-weight-bold mb-1 float-left">{{gettext("Password")}}</label>
    <div id="btnViewPW_{{id}}" class="input-group">
      <input type="password" class="form-control" name="password" value="">
      <div class="input-group-append">
        <span class="input-group-text"><i class="fa fa-eye-slash"></i></span>
      </div>
    </div>
  </div>
  <div class="form-group">
    <button type="submit" class="btn btn-primary float-right font-weight-bold">
      <i class="fas fa-sign-in-alt"></i> {{gettext("Login")}}
    </button>
  </div>
</form>
<script type="text/javascript" src="/static/webui/vendor/cryptojs/crypto-js.min.js"></script>
<script type="text/javascript">
  $(document).ready(function() {
    $("#btnViewPW_{{id}} span").bind("mousedown touchstart",function(){$("#btnViewPW_{{id}}>input").attr("type","text");$("#btnViewPW_{{id}} i").removeClass("fa-eye-slash").addClass("fa-eye")}).bind("mouseup mouseleave touchend",function(){$("#btnViewPW_{{id}}>input").attr("type","password");$("#btnViewPW_{{id}} i").removeClass("fa-eye").addClass("fa-eye-slash")});
    $("#frmLogin_{{id}}").submit(function(e){e.preventDefault();WebUI.notify.clear();var u=$("#frmLogin_{{id}} input[name=username]"),p=$("#frmLogin_{{id}} input[name=password]");WebUI.loader.load("POST","{{url}}",{_csrf_token:"{{csrf_token()}}",username:u.val(),digest:(p.val())?CryptoJS.SHA256("{{authkey}}"+CryptoJS.SHA256(p.val())).toString():""},null,null,function(){p.val("");p.focus()},200);return false});
  });
</script>
