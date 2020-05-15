<!doctype html>
<html lang="{{page_lang or 'en'}}" dir="{{page_langdir or 'ltr'}}" class="scroll">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{{page_doctitle}}</title>
  {% block b_html_head %}{% endblock %}
</head>
<body dir="{{page_langdir or 'ltr'}}" class="scroll">
  {% block b_html_body %}{% endblock %}
  <!--[if IE]>
  <script type="text/javascript">
    document.body.innerHTML = '<h2>You are using an outdated browser.</h2><p>Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>';
  </script>
  <![endif]-->
</body>
</html>
