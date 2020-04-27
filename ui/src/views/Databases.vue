<!--
#
# Copyright (C) 2020 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#
-->

<template>
  <div>
    <h2>{{$t('databases.title_mgmt')}}</h2>
    
    <!-- error message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
      <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
        <span class="pficon pficon-close"></span>
      </button>
      <span class="pficon pficon-error-circle-o"></span>
      {{ errorMessage }}.
    </div>

    <div v-if="!uiLoaded" class="spinner spinner-lg"></div>
    <div v-if="uiLoaded">
      <h3>{{$t('databases.create_database')}}</h3>
      <form class="form-horizontal" v-on:submit.prevent="createDatabase()">
        <div class="row">
          <div class="col-lg-12">
            <div :class="['form-group margintop', errors.newDatabase.hasError ? 'has-error' : '']">
              <label class="col-sm-2 control-label">
                {{$t('databases.database_name')}}
              </label>
              <div class="col-sm-5">
                <input
                  v-model="newDatabase.name"
                  type="text"
                  required
                  class="form-control"
                >
                <span v-if="errors.newDatabase.hasError" class="help-block">{{$t('databases.database_already_exists')}}</span>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 control-label">
              </label>
              <div class="col-sm-5">
                <button 
                  class="btn btn-primary margintop" 
                  type="submit"
                  :disabled="!newDatabase.name || newDatabase.isLoading"
                >
                  {{$t('databases.create')}}
                </button>
                <div
                  v-if="newDatabase.isLoading"
                  class="spinner spinner-sm form-spinner-loader marginleft"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </form>
      
      <h3>{{$t('databases.databases_details')}}</h3>
      <div class="row">
        <div class="col-lg-12">
          <div v-if="!dbList.details" class="spinner spinner-sm"></div>
          <pre v-if="dbList.details" class="prettyprint">{{dbList.details}}</pre>
        </div>
      </div>
      
      <h3>{{$t('databases.terminal_utility')}}</h3>
      <form class="form-horizontal">
        <div class="row">
          <div class="col-lg-12">
            {{$t('databases.terminal_utility_desc')}}:
            <div class="form-group margintop">
              <label class="col-sm-2 control-label">
                {{$t('databases.sqlcmd_path')}}
              </label>
              <div class="col-sm-5">
                <input
                  id="sqlcmd"
                  readonly
                  type="text"
                  class="form-control"
                  value="/opt/mssql-tools/bin/sqlcmd"
                >
              </div>
            </div>
            <div class="form-group margintop">
              <label class="col-sm-2 control-label">
              </label>
              <div class="col-sm-5">
                <button 
                  class="btn btn-primary" 
                  type="button"
                  @click="copyCmd('sqlcmd')"
                >
                  {{$t('databases.copy')}}
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
      
    </div>
  </div>
</template>

<script>
export default {
  name: "Databases",
  mounted() {
    this.getDbList();
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      errors: this.initErrors(),
      newDatabase: {
        name: null,
        isLoading: false
      },
      dbList: {
        details: null
      }
    }
  },
  methods: {
    showErrorMessage(errorMessage, error) {
      console.error(errorMessage, error) /* eslint-disable-line no-console */
      this.errorMessage = errorMessage;
    },
    closeErrorMessage() {
      this.errorMessage = null;
    },
    createDatabase() {
      var context = this;
      context.newDatabase.isLoading = true;
      
      var settingsObj = {
        action: "create-database",
        "newDatabase": {
          name: context.newDatabase.name
        }
      };
      context.loaders = true;
      context.errors = context.initErrors();
      nethserver.exec(
        ["nethserver-mssql/databases/validate"],
        settingsObj,
        null,
        function(success) {
          context.loaders = false;
          
          nethserver.notifications.success = context.$i18n.t(
            "databases.database_create_ok"
          );
          
          nethserver.notifications.error = context.$i18n.t(
            "databases.not_valid_database_name"
          );
          
          // update values
          nethserver.exec(
            ["nethserver-mssql/databases/update"],
            settingsObj,
            function(stream) {
              console.info("create-database", stream);
            },
            function(success) {
              context.newDatabase.name = null;
              context.newDatabase.isLoading = false;
            },
            function(error, data) {
              console.error(error, data);
            },
            true //sudo
          );
        },
        function(error, data) {
          var errorData = {};
          context.loaders = false;
          context.errors = context.initErrors();
          try {
            errorData = JSON.parse(data);
            for (var e in errorData.attributes) {
              var attr = errorData.attributes[e];
              context.errors[attr.parameter].hasError = true;
              context.errors[attr.parameter].message = attr.error;
            }
            context.newDatabase.isLoading = false;
          } catch (e) {
            console.error(e);
          }
        },
        true // sudo
      );
    },
    initErrors() {
      return {
        newDatabase: {
          hasError: false,
          message: ""
        }
      }
    },
    getDbList() {
      var context = this;
      context.uiLoaded = false;
      nethserver.exec(
        ["nethserver-mssql/databases/execute"],
        { action: "db-list" },
        null,
        function(success) {
          try {
            context.dbList.details = success;
          } catch (e) {
            console.error(e);
          }
          context.uiLoaded = true;
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("databases.error_reading_mssql_db_details"), error);
        }
      );
    },
    copyCmd(id) {
      var command = document.getElementById(id);      
      command.select();
      command.setSelectionRange(0, command.value.length);
      document.execCommand("copy");
    }
  }
};
</script>

<style scoped>
.margintop {
  margin-top: 15px;
}
.marginleft {
  margin-left: 20px;
}
</style>