 require.config({
    paths: {
			jquery: '../../bower_components/jquery/jquery',
			listJs: '../../bower_components/listjs/dist/list',
      listPagination: '../../bower_components/list.pagination.js/dist/list.pagination',
			fuzzySearch: '../../bower_components/list.fuzzysearch.js/dist/list.fuzzysearch',
      datepicker: '../../bower_components/bootstrap3-datetimepicker/build/js/bootstrap-datetimepicker.min',
      moment: '../../bower_components/moment/moment'
		},

		shim: {
			jquery: {
				exports: 'jquery'
			},
      listJs: {
        exports: 'List'
      },
      listPagination: {
        deps: ['listJs']
      },
			fuzzySearch: {
				deps: ['listJs']
			},
      datepicker: {
        deps: ['jquery', 'moment']
      }
		}
	});

require(['domReady', 'listJs', 'jquery', 'fuzzySearch', 'listPagination', 'datepicker'],
				function (domReady, List, $, fuzzySearch, listPagination, datepicker) {
	"use strict";

	domReady(function() {

		// List.js
		var fuzzyOptions = {
			searchClass: 'fuzzy-search',
			location: 0,
			distance: 100,
			threshold: 0.4,
			multiSearch: true
		};

		var options = {
			valueNames: ['ean', 'description'],
      listClass: "list",
      searchClass: "search",
      sortClass: "sort",
      indexAsync: "false",
      page: 10,
			plugins: [ listPagination({}), fuzzySearch() ],

		};
		var purchaseList = new List('list-purchases', options);
		var salesList = new List('list-sales', options);


    // Bootstrap Datetimepicker
    $('#datetimepicker8').datetimepicker({ language: 'lv' });
    $('#datetimepicker9').datetimepicker({ language: 'lv' });
    $("#datetimepicker8").on("change.dp",function (e) {
      $('#datetimepicker9').data("DateTimePicker").setStartDate(e.date);
    });
    $("#datetimepicker9").on("change.dp",function (e) {
      $('#datetimepicker8').data("DateTimePicker").setEndDate(e.date);
    });

	});
});

