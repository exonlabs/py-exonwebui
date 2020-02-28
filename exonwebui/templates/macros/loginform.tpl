<div class="card {{styles}}">
  <div class="card-body pt-3 pb-2">
    <form id="frmLogin">
      <div class="form-group mb-2">
        <label class="control-label font-weight-bold mb-1 float-left">{{gettext("Username")}}</label>
        <input type="text" class="form-control" name="username" value="">
      </div>
      <div class="form-group">
        <label class="control-label font-weight-bold mb-1 float-left">{{gettext("Password")}}</label>
        <input type="password" class="form-control" name="password" value="">
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary float-right font-weight-bold">
          <i class="fas fa-sign-in-alt"></i> {{gettext("Login")}}
        </button>
      </div>
    </form>
    <script type="text/javascript">
      $(document).ready(function() {
        $("#frmLogin").submit(function(e) {
          e.preventDefault(); WebUI.notify.clear();
          var u=$("#frmLogin input[name=username]"),p=$("#frmLogin input[name=password]");
          WebUI.request("POST","{{url}}",{_csrf_token:"{{csrf_token()}}",username:u.val(),
            digest:(p.val())?CryptoJS.MD5("{{authkey}}"+CryptoJS.MD5(p.val())).toString():""});
          u.focus(); p.val(""); return false;
        });
      });
    </script>
  </div>
</div>
