from django.urls import path
import olymp.views

urlpatterns = [
    path('',olymp.views.home,name = 'home'),
    path('home',olymp.views.home,name = 'home'),
    path('login',olymp.views.login,name = 'login'),
    path('user_reg',olymp.views.userRegister,name = 'user_reg'),
    path('admin_reg',olymp.views.adminRegister,name = 'admin_reg'),
    path('admin_home',olymp.views.adminHome,name = 'admin_home'),
    path('user_home',olymp.views.userHome,name = 'user_home'),
    path('logout',olymp.views.logout,name = 'logout'),

    path('olym_med_prd_usr',olymp.views.olym_med_prd_usr,name = 'olym_med_prd_usr'),
    path('delete_predict_user/<id>', olymp.views.delete_predict_user, name='delete_predict_user'),
    path('prdct_olym',olymp.views.prdct_olym,name = 'prdct_olym'),

    path('olym_med_prd_adm', olymp.views.olym_med_prd_adm, name='olym_med_prd_adm'),
    path('user_message', olymp.views.user_message, name='user_message'),
    path('user_msg_adm', olymp.views.user_msg_adm, name='user_msg_adm'),
    path('delete_message/<id>', olymp.views.delete_message, name='delete_message'),


    path('play_for_bet_adm', olymp.views.play_for_bet_adm, name='play_for_bet_adm'),
    path('delete_play_adm/<id>', olymp.views.delete_play_adm, name='delete_play_adm'),
    path('bettings_adm', olymp.views.bettings_adm, name='bettings_adm'),
    path('del_bet_adm/<id>', olymp.views.del_bet_adm, name='del_bet_adm'),
    

    path('plays_for_bet_usr', olymp.views.plays_for_bet_usr, name='plays_for_bet_usr'),
    path('coun_pass_usr/<id>', olymp.views.coun_pass_usr, name='coun_pass_usr'),
    path('coun_pass_usr1/<id>', olymp.views.coun_pass_usr1, name='coun_pass_usr1'),
    path('my_bettings_usr', olymp.views.my_bettings_usr, name='my_bettings_usr'),
    path('purchase_mon_usr', olymp.views.purchase_mon_usr, name='purchase_mon_usr'),
    path('purchase_mon_usr1', olymp.views.purchase_mon_usr1, name='purchase_mon_usr1'),
    path('add_play_adm', olymp.views.add_play_adm, name='add_play_adm'),


    path('add_fail/<id>', olymp.views.add_fail, name='add_fail'),
    path('add_pass/<id>', olymp.views.add_pass, name='add_pass'),


    
    path('trans_adm', olymp.views.trans_adm, name='trans_adm'),
    path('delete_trans_adm/<id>', olymp.views.delete_trans_adm, name='delete_trans_adm'),
    path('bet_hist_user', olymp.views.bet_hist_user, name='bet_hist_user'),
    path('delete_trans_usr/<id>', olymp.views.delete_trans_usr, name='delete_trans_usr'),


    path('m_to_b_adm', olymp.views.m_to_b_adm, name='m_to_b_adm'),
    path('m_from_b_adm', olymp.views.m_from_b_adm, name='m_from_b_adm'),
    path('m_to_b_usr', olymp.views.m_to_b_usr, name='m_to_b_usr'),
    path('m_from_b_usr', olymp.views.m_from_b_usr, name='m_from_b_usr'),
    path('purchase_mon_adm', olymp.views.purchase_mon_adm, name='purchase_mon_adm'),



    




]