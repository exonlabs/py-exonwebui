{% macro _group_items(items) %}
  {% for k in items %}
    {% if k.type == 'text' %}
      <span class="input-group-text">{{k.value|safe}}</span>
    {% elif k.type == 'icon' %}
      <span class="input-group-text"><i class="fa fas {{k.value}}"></i></span>
    {% elif k.type == 'select' %}
      <select class="custom-select" name="{{k.name}}">
        {% for o in k.options %}<option value="{{o.value}}" {{'selected' if o.selected else ''}}>{{o.label}}</option>{% endfor %}
      </select>
    {% endif %}
  {% endfor %}
{% endmacro %}

<script type="text/javascript">
  WebUI.loadCss.after("/static/webui/css/webui_inputform.min.css","link[href$='webui.min.css']");
</script>
<form id="form_{{id}}" class="form-wrapper {{styles}}" method="POST" action="{{submit_url}}" novalidate>
  {% for f in fields %}
    {% if f.type == 'hidden' %}
      <input type="hidden" name="{{f.name}}" value="{{f.value}}">
    {% elif f.type == 'title' %}
      <div class="form-title text-muted py-2">{{f.label|safe}}</div>
    {% else %}
      <div class="form-row form-group">
        <label class="col-11 col-sm-3 col-form-label text-nowrap {{'required' if f.required and f.type != 'static' else ''}}">{{f.label|safe}}</label>
        {% if f.helpguide and f.type != 'static' %}
          <div class="col-1 col-sm-1 order-sm-12 mt-2 text-left text-info">
            <a class="btn_helpguide" data-helpguide="{{f.helpguide|safe}}"><i class="fa fas fa-fw fa-lg fa-question-circle"></i></a>
          </div>
        {% endif %}
        <div class="col-12 col-sm-8">
          {% if f.type == 'custom' %}
            {{f.value|safe}}
          {% elif f.type == 'static' %}
            <input type="text" class="form-control-plaintext" value="{{f.value}}" readonly>
          {% elif f.type in ['checkbox','radio'] %}
            {% for o in f.options %}
              <div class="form-check {{'pt-1' if loop.first else ''}}">
                <input type="{{f.type}}" class="form-check-input" name="{{o.name if f.type=='checkbox' else f.name}}" value="{{1 if f.type=='checkbox' else o.value}}" {{'checked' if o.selected else ''}} {{'disabled' if o.disabled else ''}} {{'required' if f.required else ''}}>
                <label class="form-check-label px-1">{{o.label}}</label>
              </div>
            {% endfor %}
          {% elif f.type == 'password' %}
            <div class="input-group">
              {% if f.prepend %}<div class="input-group-prepend">{{_group_items(f.prepend)}}</div>{% endif %}
              <input type="password" class="form-control" name="{{f.name}}" value="" placeholder="{{f.placeholder}}" {% if f.strength %}data-plugin="passStrengthify"{% endif %} {% if f.confirm %}data-confirm="{{f.name}}"{% endif %} {{'required' if f.required else ''}}>
              <div class="input-group-append">
                {% if f.append %}{{_group_items(f.append)}}{% endif %}
                <span class="input-group-text" data-pwdview="{{f.name}}"><i class="fa fas fa-eye-slash"></i></span>
              </div>
            </div>
            {% if f.confirm %}
              <div class="input-group pt-1">
                <div class="input-group-prepend">
                  <span class="input-group-text">{{gettext('Confirm')}}</span>
                </div>
                <input type="password" class="form-control" name="{{f.name}}_confirm" data-confirm="{{f.name}}" value="" placeholder="{{f.placeholder}}" {{'required' if f.required else ''}}>
                <div class="input-group-append">
                  <span class="input-group-text" data-pwdview="{{f.name}}_confirm"><i class="fa fas fa-eye-slash"></i></span>
                </div>
              </div>
            {% endif %}
          {% elif f.type in ['date','time','datetime'] %}
            <div class="input-group">
              {% if f.prepend %}<div class="input-group-prepend">{{_group_items(f.prepend)}}</div>{% endif %}
              <input type="text" class="form-control" name="{{f.name}}" value="{{f.value}}" placeholder="{{f.placeholder}}" data-plugin="datetimepicker" data-format="{% if f.format %}{{f.format}}{% elif f.type=='date' %}YYYY-MM-DD{% elif f.type=='time' %}HH:mm:00{% else %}YYYY-MM-DD HH:mm:00{% endif %}" {{'required' if f.required else ''}}>
              <div class="input-group-append">
                {% if f.append %}{{_group_items(f.append)}}{% endif %}
                <span class="input-group-text"><i class="fa fas fa-fw {{'fa-clock fa-clock-o' if f.type=='time' else 'fa-calendar fa-calendar-alt'}}"></i></span>
              </div>
            </div>
          {% elif f.type == 'file' %}
            <div class="input-group">
              {% if f.prepend %}<div class="input-group-prepend">{{_group_items(f.prepend)}}</div>{% endif %}
              <div class="custom-file">
                <input type="file" class="custom-file-input" name="{{f.name}}" {% if f.format %}accept="{{f.format}}"{% endif %} placeholder="{{f.placeholder if f.placeholder else gettext('Select files')}}" data-plugin="bsCustomFileInput" data-maxsize="{{f.maxsize}}" {{'multiple' if f.multiple else ''}} {{'required' if f.required else ''}}>
                <label class="custom-file-label text-truncate empty">{{f.placeholder if f.placeholder else gettext('Select files')}}</label>
              </div>
              <div class="input-group-append">
                <span class="input-group-text text-danger d-none" data-fileerror="{{f.name}}"></span>
                <button class="input-group-text" data-fileselect="{{f.name}}">{{gettext('Browse')}}</button>
                {% if f.append %}{{_group_items(f.append)}}{% endif %}
              </div>
            </div>
          {% else %}
            <div class="input-group">
              {% if f.prepend %}<div class="input-group-prepend">{{_group_items(f.prepend)}}</div>{% endif %}
              {% if f.type == 'text' %}
                <input type="text" class="form-control" name="{{f.name}}" value="{{f.value}}" placeholder="{{f.placeholder}}" {{'required' if f.required else ''}}>
              {% elif f.type == 'textarea' %}
                <textarea class="form-control scroll" name="{{f.name}}" rows="{{f.rows}}" placeholder="{{f.placeholder}}" {{'required' if f.required else ''}}>{{f.value}}</textarea>
              {% elif f.type == 'select' %}
                <select class="custom-select scroll" name="{{f.name}}" {% if f.multiple %}multiple {% if f.rows %}size="{{f.rows}}"{% endif %}{% endif %} {{'required' if f.required else ''}}>
                  {% for o in f.options %}
                    <option value="{{'' if o.value==None else o.value}}" {{'selected' if o.selected or (not f.multiple and loop.first and o.value==None) else ''}} {{'disabled' if o.disabled or (loop.first and o.value==None) else ''}}>{{o.label}}</option>
                  {% endfor %}
                </select>
              {% endif %}
              {% if f.append %}<div class="input-group-append">{{_group_items(f.append)}}</div>{% endif %}
            </div>
          {% endif %}
          {% if f.help and f.type != 'static' %}<i class="form-text text-muted">{{f.help|safe}}</i>{% endif %}
        </div>
      </div>
    {% endif %}
  {% endfor %}
</form>
<script type="text/javascript">
  $(document).ready(function(){
    if($("#form_{{id}} input[data-plugin='passStrengthify']").length){
      WebUI.loadScript("/static/webui/vendor/js/passstrength.min.js",function(){
        $("#form_{{id}} input[data-plugin='passStrengthify']").each(function(){
          $(this).passStrengthify({minimum:1,security:1})});
      });
    };
    if($("#form_{{id}} input[data-plugin='datetimepicker']").length){
      WebUI.loadCss.before("/static/webui/vendor/datetimepicker/datetimepicker.min.css","link[href$='webui_inputform.min.css']");
      WebUI.loadScript("/static/webui/vendor/js/moment.min.js",function(){
      WebUI.loadScript("/static/webui/vendor/datetimepicker/datetimepicker.min.js",function(){
        $("#form_{{id}} input[data-plugin='datetimepicker']").each(function(){
          $(this).datetimepicker({format:$(this).data('format'),useCurrent:true,showClear:true,showClose:true})});
      })});
    };
    if($("#form_{{id}} input[data-plugin='bsCustomFileInput']").length){
      WebUI.loadScript("/static/webui/vendor/js/bs-custom-file-input.min.js",function(){
        bsCustomFileInput.init("#form_{{id}} input[data-plugin='bsCustomFileInput']");
        $("#form_{{id}} input[data-plugin='bsCustomFileInput']").on("change",function(e){
          var m=parseInt($(this).data('maxsize')),fsizechk=true;
          if($(this).val()){
            $(this).next(".custom-file-label").removeClass('empty');
            for(const f of $(this)[0].files) if(m>0 && f.size>m) fsizechk=false;
          }
          else {
            $(this).next(".custom-file-label").addClass('empty').html($(this).attr("placeholder"));
          };
          $("#form_{{id}} button[data-fileselect="+$(this).attr('name')+"]")
            .html($(this).val()?'<b>&times;</b>':'{{gettext("Browse")}}');
          if(fsizechk) {
            $(this).get(0).setCustomValidity('');
            $("#form_{{id}} span[data-fileerror="+$(this).attr('name')+"]")
              .html('').addClass('d-none')
          }else{
            $(this).get(0).setCustomValidity('Invalid');
            $("#form_{{id}} span[data-fileerror="+$(this).attr('name')+"]")
              .html('{{gettext("Too Large File")}}').removeClass('d-none');
          };
        });
        $("#form_{{id}} button[data-fileselect]").on("click",function(e){
          e.preventDefault();
          var sel=$("#form_{{id}} input[name="+$(this).data('fileselect')+"]");
          if(sel.val()) sel.val('').trigger('change'); else sel.trigger('click');
          return false;
        });
      });
    };
    $("#form_{{id}} input[data-confirm]").on("click change keypress keyup keydown touchstart touchend",function(){
      var m=$("#form_{{id}} input[name="+$(this).data('confirm')+"]"),
        c=$("#form_{{id}} input[name="+$(this).data('confirm')+"_confirm]");
      c.get(0).setCustomValidity((m.val()==c.val())?'':'Invalid');
    });
    $("#form_{{id}} span[data-pwdview]")
      .on("mousedown touchstart",function(){
        $("#form_{{id}} input[name="+$(this).data("pwdview")+"]").attr("type","text");
        $(this).children("i").removeClass("fa-eye-slash").addClass("fa-eye")})
      .on("mouseup mouseleave touchend",function(){
        $("#form_{{id}} input[name="+$(this).data("pwdview")+"]").attr("type","password");
        $(this).children("i").removeClass("fa-eye").addClass("fa-eye-slash")});
    $("#form_{{id}} select:not([multiple])").on("change",function(){
      if($(this).find(":selected").val()) $(this).removeClass("empty"); else $(this).addClass("empty");
    }).trigger('change');
    $("#form_{{id}} a.btn_helpguide").on("click",function(e){
      e.preventDefault();
      WebUI.pagelock.modal(
        '<h5 class="m-0 py-2 text-info"><i class="fa fas fa-fw fa-question-circle"></i> {{gettext("Quick Guide")}}</h5>',
        '<p class="">'+$(this).data('helpguide')+'</p>',
        '<button class="btn btn-primary" onclick="WebUI.pagelock.hide()">{{gettext("Got it")}}</button>');
      return false;
    });
    $("#form_{{id}}").on('submit',function(e){
      e.preventDefault();
      WebUI.notify.clear();
      WebUI.scrolltop();
      $(this).removeClass('was-validated').find("input").removeClass('is-invalid');
      if(this.checkValidity()===false){
        $(this).addClass('was-validated');
        WebUI.notify.error('{{gettext("Please fill all required fields")}}');
      }else{
        WebUI.loader.formsubmit($(this),function(result){
          if(result.validation){
            for(var i=0;i<result.validation.length;i++)
              $("#form_{{id}} input[name='"+result.validation[i]+"']").addClass('is-invalid');
          };
          WebUI.request.success(result);
        },null,null,500);
      };
      return false;
    });
    $("#form_{{id}}").on('reset',function(e){
      WebUI.notify.clear();
      WebUI.scrolltop();
      $(this).removeClass('was-validated');
      $(this)[0].reset();
      $(this).find("input").removeClass('is-valid is-invalid').trigger('change').trigger('keyup');
    });
  });
</script>
