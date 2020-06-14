<div id="DataGrid_wrapper_{{id}}" class="card datagrid-wrapper {{styles}}">
  <div class="card-header p-2">
    <div class="float-left overflow-hidden pt-1 px-2">
      <h5 class="my-0 text-dark">{{title|safe}}</h5>
    </div>
    <div class="float-right p-0">
      <div class="btn-group">
        <div id="btnDataGridExp_{{id}}" class="btn-group">
          <button class="btn btn-sm btn-light text-secondary px-1 py-0" data-toggle="dropdown" title="{{gettext('Export')}}">
            <i class="fas fa-file-export"></i></button>
          <div class="dropdown-menu dropdown-menu-right p-0 pb-1" style="min-width:100px">
            <h6 class="dropdown-header px-3">{{gettext("Export")}}</h6>
            <button id="btnExpCSV_{{id}}" class="dropdown-item pl-3 pr-4 py-1">
              <i class="fas fa-fw fa-file-csv"></i> {{gettext("csv")}}</button>
            <button id="btnExpXLS_{{id}}" class="dropdown-item pl-3 pr-4 py-1">
              <i class="fas fa-fw fa-file-excel"></i> {{gettext("xls")}}</button>
            <button id="btnPRINT_{{id}}" class="dropdown-item pl-3 pr-4 py-1">
              <i class="fas fa-fw fa-print"></i> {{gettext("print")}}</button>
          </div>
        </div>
        <div id="btnDataGridVis_{{id}}" class="btn-group">
          <button class="btn btn-sm btn-light text-secondary px-1 py-0" data-toggle="dropdown" title="{{gettext('Columns')}}">
            <i class="fas fa-th-list"></i></button>
          <div class="dropdown-menu dropdown-menu-right p-0" style="min-width:100px">
            <h6 class="dropdown-header px-3">{{gettext("Show / Hide")}}</h6>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="card-body">
    <table id="tblDataGrid_{{id}}" class="table table-sm table-hover text-nowrap w-100">
    </table>
  </div>
</div>
<script type="text/javascript">
  $(document).ready(function() {
    function getFileName(){
      var tz = (new Date()).getTimezoneOffset()*60000;
      var ts = (new Date(Date.now()-tz)).toISOString().slice(0,19)
        .replaceAll('T','').replaceAll('-','').replaceAll(':','');
      return '{{export_prefix}}_'+ts;
    };
    $.fn.dataTable.ext.errMode = 'none';
    $.fn.DataTable.ext.pager.numbers_length = 5;
    var dt = $("#tblDataGrid_{{id}}").DataTable({
      dom: '<"float-right ml-1"l><"float-right"f><"table-responsive scroll"t><"float-left"i><"float-right pt-2"p>',
      colReorder:true, pagingType:"full_numbers", stateSave:true,
      lengthMenu:[[{{lenMenu|join(',')}}],[{{lenMenu|join(',')|replace('-1','"'|safe+gettext("All")+'"'|safe)}}]],
      select:{style:'multi+shift',selector:'td.select-checkbox'},
      columns:[
        {defaultContent:'',searchable:false,orderable:false,className:'dtctrl table-index px-0'},
        {defaultContent:'',searchable:false,orderable:false,className:'dtctrl select-checkbox px-3'},
        {{columns|safe}}
      ],
      order:[[2,'asc']],
      buttons:{
        dom:{button:{className:'dropdown-item pl-3 pr-4 py-0 text-left tick-select'}},
        buttons:[
          {extend:'columnsToggle',columns:':not(.dtctrl)'},
          {extend:'csvHtml5',className:'d-none',title:'{{title}}',
           filename:getFileName,exportOptions:{columns:':visible:not(.dtctrl)'}},
          {extend:'excelHtml5',className:'d-none',title:null,
           filename:getFileName,exportOptions:{columns:':visible:not(.dtctrl)'}},
          {extend:'print',className:'d-none',title:'{{title}}',
           exportOptions:{columns:':visible:not(.dtctrl)'}},
        ]
      },
      language:{
        search: '<i title="{{gettext("Search")}}" class="fas fa-search"></i>',
        lengthMenu: '_MENU_',
        info: "{{gettext('Showing _START_-_END_ of _TOTAL_')}}",
        infoEmpty: "",
        infoFiltered: "",
        emptyTable: "{{gettext('No data available')}}",
        zeroRecords: "{{gettext('No matching records found')}}",
        paginate:{
          first:'<i class="fa fa-angle-double-left"></i>',
          last:'<i class="fa fa-angle-double-right"></i>',
          previous:'<i class="fa fa-angle-left"></i>',
          next:'<i class="fa fa-angle-right"></i>'},
        select:{rows:'',columns:'',cells:''},
      }
    });
    dt.buttons().container().appendTo('#btnDataGridVis_{{id}}>.dropdown-menu');
    $('#btnDataGridVis_{{id}}>.dropdown-menu').on("click",function(e){e.stopPropagation()});
    $(dt.column(1).header()).on("click",function(){
      $(this).toggleClass('selected');
      if($(this).hasClass('selected')) dt.rows().select(); else dt.rows().deselect();
    });

    //exports
    $('#btnExpCSV_{{id}}').click(function(){dt.button('.buttons-csv').trigger()});
    $('#btnExpXLS_{{id}}').click(function(){dt.button('.buttons-excel').trigger()});
    $('#btnPRINT_{{id}}').click(function(){dt.button('.buttons-print').trigger()});

    // events
    dt.on('error.dt', function(e,s,t,msg){WebUI.notify.error(msg)});
    dt.on('order.dt search.dt',function(){
      dt.column(0,{search:'applied',order:'applied'}).nodes().each(function(cell,i){cell.innerHTML=i+1});
    }).draw();
    dt.on('select deselect', function(){
      if(dt.rows({selected:true}).count()>0) $(dt.column(1).header()).addClass('selected');
      else $(dt.column(1).header()).removeClass('selected');
    });

    // load data
    WebUI.loader.load("POST","{{url}}",{_csrf_token:"{{csrf_token()}}",op:"loaddata"},
      function(r){dt.rows.add(r.payload).draw()},null,null,500);
  });
</script>
