# -*- coding: utf-8 -*- 


from pyerp.fnd.gbl import fnd_global
from pyerp.fnd.models import ProfileOption, ProfileOptionValues
from pyerp.fnd.utils.version import get_svn_revision, get_version

__svnid__ = '$Id$'
__svn__ = get_svn_revision(__name__)


class Profile(object):
    def __init__(self):
        pass
    
    #
    # DEFINED - returns TRUE if a profile option has been stored
    # 
    def define(self, name):
        option = ProfileOption()
        option.name = name
        # ==============================
        option.created_by = fnd_global.user_id
        option.last_updated_by = fnd_global.user_id
        # ==============================
        option.save()
        return True
    
    #
    # SAVE - sets the value of a profile option permanently
    #        to the database, at any level.  This routine can be used
    #        at runtime or during patching.  This routine will not
    #        actually commit the changes; the caller must commit.
    #
    #        ('SITE', 'APPL', 'RESP', 'USER', 'SERVER', or 'ORG').
    #
    #        Examples of use:
    #        FND_PROFILE.SAVE('P_NAME', 'P_VAL', 'SITE');
    #        FND_PROFILE.SAVE('P_NAME', 'P_VAL', 'APPL'  , 321532);
    #        FND_PROFILE.SAVE('P_NAME', 'P_VAL', 'RESP'  , 321532);
    #        FND_PROFILE.SAVE('P_NAME', 'P_VAL', 'USER'  , 123321);
    #        FND_PROFILE.SAVE('P_NAME', 'P_VAL', 'SERVER', 25    );
    #        FND_PROFILE.SAVE('P_NAME', 'P_VAL', 'ORG'   , 204   );
    #
    #  returns: TRUE if successful, FALSE if failure.
    #
    #
    def save(self, 
             x_name,               # /* Profile name you are setting */
             x_option_value,       # /* Profile value you are setting */
             x_level_id,           # /* Level that you're setting at: 'SITE','APPL','RESP','USER', etc. */
             x_level_value=0):     # /* Level value that you are setting at, e.g. user id for 'USER' level. X_LEVEL_VALUE is not used at site level. */
        option = ProfileOption.objects.get(name=x_name)
        value = ProfileOptionValues()
        value.option = option
        value.level_id = x_level_id
        value.level_value = x_level_value
        value.option_value = x_option_value
        # ==============================
        value.created_by = fnd_global.user_id
        value.last_updated_by = fnd_global.user_id
        # ==============================
        value.save()
        return True
    
    #
    # VALUE - returns the value of a profile options
    #
    #
    # Works exactly like GET, except it returns the value of the
    # specified profile option as a function result.
    # @param name Profile name
    # @return specified profile option value
    # @rep:scope public
    # @rep:displayname Get Profile Value
    # @rep:compatibility S
    # @rep:lifecycle active
    # @rep:ihelp FND/@prof_plsql See related online help.
    #
    def value(self, x_name):
        # if (x_option.hierarchy_type=="SECURITY"):
        #   # USER
        #   if (x_option.al_user_visible):
        #     return 
        #   # RESP
        #   if (x_option.al_resp_visible):
        #     return 
        #   # APPLICATION
        #   if (x_option.al_app_visible):
        #     return 
        #   # SITE
        #   if (x_option.al_site_visible):
        #     return 
        # elif (x_option.hierarchy_type=="SERVER"):
        #   # USER
        #   if (x_option.al_user_visible):
        #     return 
        #   # SERVER
        #   if (x_option.al_server_visible):
        #     return 
        #   # SITE
        #   if (x_option.al_site_visible):
        #     return 
        # elif (x_option.hierarchy_type=="ORGANIZATION"):
        #   # USER
        #   if (x_option.al_user_visible):
        #     return 
        #   # ORGANIZATION
        #   if (x_option.al_org_visible):
        #     return 
        #   # SITE
        #   if (x_option.al_site_visible):
        #     return 
        # return None
      
        x_option = ProfileOption.objects.get(name=x_name)
        # USER
        if (fnd_global.user_id!=-1):
            try:
                v = ProfileOptionValues.objects.get(option=x_option, level_id='USER', level_value=fnd_global.user_id)
                return v.option_value
            except ProfileOptionValues.DoesNotExist:
                pass
    
        # RESP
        if (fnd_global.resp_id!=-1):
            try:
                v = ProfileOptionValues.objects.get(option=x_option, level_id='RESP', level_value=fnd_global.resp_id)
                return v.option_value
            except ProfileOptionValues.DoesNotExist:
                pass
    
        # ORG
    #    if (fnd_global.org_id!=-1):
    #        try:
    #            v = ProfileOptionValues.objects.get(option=x_option, level_id='ORG', level_value=fnd_global.org_id)
    #            return v.option_value
    #        except ProfileOptionValues.DoesNotExist:
    #            pass
      
        # SERVER
        if (fnd_global.get_server_id!=-1):
            try:
                v = ProfileOptionValues.objects.get(option=x_option, level_id='APPL', level_value=fnd_global.get_server_id)
                return v.option_value
            except ProfileOptionValues.DoesNotExist:
                pass
    
        # APPL
        if (fnd_global.appl_id!=-1):
            try:
                v = ProfileOptionValues.objects.get(option=x_option, level_id='APPL', level_value=fnd_global.appl_id)
                return v.option_value
            except ProfileOptionValues.DoesNotExist:
                pass
    
        # SITE
        if (fnd_global.site_id!=-1):
            try:
                v = ProfileOptionValues.objects.get(option=x_option, level_id='SITE', level_value=fnd_global.site_id)
                return v.option_value
            except ProfileOptionValues.DoesNotExist:
                pass
    
        return None
    
    #
    # DELETE - deletes the value of a profile option permanently from the
    #          database, at any level.  This routine serves as a wrapper to
    #          the SAVE routine which means that this routine can be used at
    #          runtime or during patching.  Like the SAVE routine, this
    #          routine will not actually commit the changes; the caller must
    #          commit.
    #
    #        ('SITE', 'APPL', 'RESP', 'USER', 'SERVER', or 'ORG').
    #
    #        Examples of use:
    #        FND_PROFILE.DELETE('P_NAME', 'SITE');
    #        FND_PROFILE.DELETE('P_NAME', 'APPL', 321532);
    #        FND_PROFILE.DELETE('P_NAME', 'RESP', 321532, 345234);
    #        FND_PROFILE.DELETE('P_NAME', 'USER', 123321);
    #        FND_PROFILE.DELETE('P_NAME', 'SERVER', 25);
    #        FND_PROFILE.DELETE('P_NAME', 'ORG', 204);
    #
    #  returns: TRUE if successful, FALSE if failure.
    #
    #
    def delete(self, 
               x_name,                       # /* Profile name you are setting */
               x_level_name,                 # /* Level that you're setting at: 'SITE','APPL','RESP','USER', etc. */
               x_level_value=0):             # /* Level value that you are setting at, e.g. user id for 'USER' level.X_LEVEL_VALUE is not used at site level. */
        return boolean;
    
    #
    def __getitem__(self, key):
        return self.value(key)

fnd_profile = Profile()
