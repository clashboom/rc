 require.config({
     paths: {
         jquery: '/bower_components/jquery/jquery',
         listJs: '/bower_components/listjs/dist/list',
         fuzzySearch: '/bower_components/list.fuzzysearch.js/dist/list.fuzzysearch',
         // listPagination: '/bower_components/list.pagination.js/dist/list.pagination',
         datepicker: '/bower_components/bootstrap3-datetimepicker/build/js/bootstrap-datetimepicker.min',
         moment: '/bower_components/moment/moment'
     },

		shim: {
			// jquery: {
			// 	exports: 'jquery'
			// },
			fuzzySearch: {
				deps: ['listJs']
			},
      datepicker: {
        deps: ['jquery', 'moment']
      }
		}
	});

require(['domReady', 'listJs', 'jquery', 'fuzzySearch', 'datepicker'],
				function (domReady, List, $, fuzzySearch, datepicker) {
	"use strict";

	domReady(function() {

		// List.js
		var fuzzyOptions = {
			distance: 100,
			location: 0,
			multiSearch: true,
			searchClass: 'fuzzy-search',
			threshold: 0.4
		};

		var options = {
			valueNames: ['ean', 'description'],
      listClass: "list",
      searchClass: "search",
      sortClass: "sort",
      indexAsync: true,
      page: 10000,
			plugins: [ fuzzySearch() ]
		};


    var ViestursOut = new List('0063-sales', options)
    var ViestursIn = new List('0063-purchases', options)
    var IlgaOut = new List('0040-sales', options)
    var IlgaIn = new List('0040-purchases', options)
    var SigitaOut = new List('0000-sales', options)
    var SigitaIn = new List('0000-purchases', options)
    var DaigaOut = new List('0084-sales', options)
    var DaigaIn = new List('0084-purchases', options)
    var IvarsOut = new List('0704-sales', options)
    var IvarsIn = new List('0704-purchases', options)
    var IngaOut = new List('1360-sales', options)
    var IngaIn = new List('1360-purchases', options)
    var NonekaOut = new List('None-sales', options)
    var NonekaIn = new List('None-purchases', options)


    // Tabs

    // $("#tab-0063").addClass("active in");
    // $('#myTab a[href="#tab-0063"]').parent().addClass("active");

    $('#myTab a[href="#tab-0063').tab('show');
    $('#myTab a[href="#tab-0040"]').tab('show');
    $('#myTab a[href="#tab-0000"]').tab('show');
    $('#myTab a[href="#tab-0084"]').tab('show');
    $('#myTab a[href="#tab-0704"]').tab('show');
    $('#myTab a[href="#tab-1360"]').tab('show');


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

