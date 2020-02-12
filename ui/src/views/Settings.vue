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
    <h2>{{$t('settings.title')}}</h2>
    
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
      <form class="form-horizontal" v-on:submit.prevent="saveConfig()">
        <div class="row">
          <div class="col-lg-12">
            <div :class="['form-group margintop', errors.ProductId.hasError ? 'has-error' : '']">
              <label class="col-sm-2 control-label">
                {{$t('settings.mssql_edition')}}
                <doc-info
                  :placement="'top'"
                  :title="$t('settings.mssql_edition')"
                  :chapter="'MssqlEdition'"
                  :inline="true"
                ></doc-info>
              </label>
              <div class="col-sm-5">
                <select
                  required
                  v-model="configuration.ProductId"
                  class="combobox form-control"
                >
                  <option value="evaluation">Evaluation</option>
                  <option value="developer">Developer</option>
                  <option value="express">Express</option>
                  <option value="web">Web</option>
                  <option value="standard">Standard</option>
                  <option value="enterprise">Enterprise</option>
                  <option value="key">{{$t('settings.insert_a_key')}}</option>
                </select>
                <span v-if="errors.ProductId.hasError" class="help-block">{{$t('settings.not_valid_edition')}}</span>
              </div>
            </div>
            <div :class="['form-group margintop', errors.ProductKey.hasError ? 'has-error' : '']">
              <label class="col-sm-2 control-label"></label>
              <div class="col-sm-5">
                <input
                  v-model="configuration.ProductKey"
                  type="text"
                  class="form-control"
                  :disabled="configuration.ProductId != 'key'"
                  :placeholder="$t('settings.product_key')"
                >
                <span v-if="errors.ProductKey.hasError" class="help-block">{{$t('settings.not_valid_key')}}</span>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-2 control-label">
              </label>
              <div class="col-sm-5">
                <button 
                  class="btn btn-primary margintop" 
                  type="submit"
                  :disabled="configuration.ProductId == 'key' && configuration.ProductKey == ''"
                >
                  {{$t('save')}}
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
      <div v-if="configuration.installed && configuration.isrunning" class="margintop">
        <h3>{{$t('settings.sa_user_mgmt')}}</h3>
        <form class="form-horizontal">
          <div class="row">
            <div class="col-lg-12">
              <div class="form-group margintop">
                <label class="col-sm-2 control-label">
                  {{$t('settings.sa_password')}}
                  <doc-info
                    :placement="'top'"
                    :title="$t('settings.sa_password')"
                    :chapter="'SaPassword'"
                    :inline="true"
                  ></doc-info>
                </label>
                <div class="col-sm-5">
                  <input
                    v-model="configuration.sapassword"
                    :type="togglePass ? 'text' : 'password'"
                    class="form-control"
                    disabled
                  >
                </div>
                <div class="col-sm-2">
                  <button
                    @click="togglePassword()"
                    type="button"
                    class="btn btn-primary adjust-top-min"
                  >
                    <span :class="[!togglePass ? 'fa fa-eye' : 'fa fa-eye-slash']"></span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-2 control-label">
                </label>
                <div class="col-sm-5">
                  <button 
                    class="btn btn-primary margintop" 
                    type="button"
                    @click="openChangePassword()"
                  >
                    {{$t('settings.change_password')}}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
      <div v-else-if="configuration.installed" class="margintop">
        <div class="alert alert-warning">
          <span class="pficon pficon-warning-triangle-o"></span>
          <strong>{{$t('settings.mssql_is_not_running')}}:</strong>
          {{$t('settings.check_sql_service')}}.
        </div>
      </div>
    </div>
  </div>
  
  <div class="modal" id="changePwdModal" tabindex="-1" role="dialog" data-backdrop="static">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">
            {{$t('settings.change_sa_password')}}
          </h4>
        </div>
        <div class="alert alert-info">
          <span class="pficon pficon pficon-info"></span>
          <strong>{{$t('settings.notice')}}:</strong>
          {{$t('settings.password_must_respect_criteria')}} <a href='https://docs.microsoft.com/en-US/sql/relational-databases/security/password-policy' target='_blank'>{{$t('settings.here')}}</a>.
        </div>
        <form
          class="form-horizontal"
          v-on:submit.prevent="changePassword()"
        >
          <div class="modal-body">
            <div :class="['form-group margintop', errors.newPassword.hasError ? 'has-error' : '']">
              <label class="col-sm-2 control-label">
                {{$t('settings.password')}}
              </label>
              <div class="col-sm-5">
                <input
                  v-model="sauser.newPassword"
                  :type="toggleNewPass ? 'text' : 'password'"
                  class="form-control"
                  required
                >
                <span v-if="errors.newPassword.hasError" class="help-block">{{$t('settings.not_valid_password')}}</span>
              </div>
              <div class="col-sm-2">
                <button
                  tabindex="-1"
                  @click="toggleNewPassword()"
                  type="button"
                  class="btn btn-primary adjust-top-min"
                >
                  <span :class="[!toggleNewPass ? 'fa fa-eye' : 'fa fa-eye-slash']"></span>
                </button>
              </div>
            </div>
            <div :class="['form-group margintop', errors.confirmNewPassword.hasError ? 'has-error' : '']">
              <label class="col-sm-2 control-label">
                {{$t('settings.confirm_password')}}
              </label>
              <div class="col-sm-5">
                <input
                  v-model="sauser.confirmNewPassword"
                  :type="toggleNewPass ? 'text' : 'password'"
                  class="form-control"
                  required
                >
                <span v-if="errors.confirmNewPassword.hasError" class="help-block">{{$t('settings.not_equal_password')}}</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-default" type="button" data-dismiss="modal">{{$t('cancel')}}</button>
            <button 
              class="btn btn-primary" 
              type="submit"
              :disabled="sauser.newPassword != sauser.confirmNewPassword"
            >
              {{$t('edit')}}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Settings",
  mounted() {
    this.getConfig()
  },
  data() {
    return {
      uiLoaded: false,
      errorMessage: null,
      configuration: {
        ProductId: "express",
        ProductKey: null,
        installed: false,
        isrunning: false,
        sapassword: null
      },
      sauser: {
        newPassword: null,
        confirmNewPassword: null
      }
      errors: this.initErrors(),
      togglePass: false,
      toggleNewPass: false
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
    getConfig() {
      var context = this;
      context.uiLoaded = false;
      nethserver.exec(
        ["nethserver-mssql/settings/read"],
        { action: "configuration" },
        null,
        function(success) {
          try {
            context.configuration = JSON.parse(success).configuration;
          } catch (e) {
            console.error(e);
          }
          context.uiLoaded = true;
        },
        function(error) {
          context.showErrorMessage(context.$i18n.t("settings.error_reading_mssql_configuration"), error);
        }
      );
    },
    saveConfig() {
      var context = this;
      var settingsObj = {
        action: "edit",
        "configuration": {
          ProductId: context.configuration.ProductId,
          ProductKey: context.configuration.ProductKey
        }
      };
      context.loaders = true;
      context.errors = context.initErrors();
      nethserver.exec(
        ["nethserver-mssql/settings/validate"],
        settingsObj,
        null,
        function(success) {
          context.loaders = false;
          
          nethserver.notifications.success = context.$i18n.t(
            "settings.settings_updated_ok"
          );
          
          nethserver.notifications.error = context.$i18n.t(
            "settings.settings_updated_error"
          );
          
          // update values
          nethserver.exec(
            ["nethserver-mssql/settings/update"],
            settingsObj,
            function(stream) {
              console.info("nethserver-mssql-save", stream);
            },
            function(success) {
              context.getConfig();
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
          } catch (e) {
            console.error(e);
          }
        },
        true // sudo
      );
    },
    changePassword() {
      var context = this;
      var settingsObj = {
        action: "change-password",
        "password": {
          newPassword: context.sauser.newPassword,
          confirmNewPassword: context.sauser.confirmNewPassword
        }
      };
      context.loaders = true;
      context.errors = context.initErrors();
      nethserver.exec(
        ["nethserver-mssql/settings/validate"],
        settingsObj,
        null,
        function(success) {
          context.loaders = false;
          
          nethserver.notifications.success = context.$i18n.t(
            "settings.password_updated_ok"
          );
          
          nethserver.notifications.error = context.$i18n.t(
            "settings.not_valid_password"
          );
          
          // update values
          nethserver.exec(
            ["nethserver-mssql/settings/update"],
            settingsObj,
            function(stream) {
              console.info("nethserver-mssql-change-password", stream);
            },
            function(success) {
              context.getConfig();
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
          } catch (e) {
            console.error(e);
          }
        },
        true // sudo
      );
    },
    initErrors() {
      return {
        ProductId: {
          hasError: false,
          message: ""
        },
        ProductKey: {
          hasError: false,
          message: ""
        },
        newPassword: {
          hasError: false,
          message: ""
        },
        confirmNewPassword: {
          hasError: false,
          message: ""
        }
      }
    },
    togglePassword() {
      this.togglePass = !this.togglePass;
    },
    toggleNewPassword() {
      this.toggleNewPass = !this.toggleNewPass;
    }
  }
};
</script>

<style scoped>
.margintop {
  margin-top: 15px;
}
</style>