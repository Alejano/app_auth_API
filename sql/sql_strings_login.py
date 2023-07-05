class SqlStrings():
 
    qry_login_pgsql =  \
    """
        select *
        from nacional.vwusersacces vp2
        where  vp2.username='{}' and vp2.password='{}';
    """

    qry_version_pgsql =  \
    """
        select version
        from nacional.o_apk;
    """

    qry_o_users_pgsql =  \
    """
        select *
        from nacional.o_users vp2
        where  vp2.userid={};
    """

    qry_preregistro_pgsql =  \
    """
        select *
        from nacional.vwpreregistros vp2
        where  vp2.telefono='{}';
    """

    ins_token_pgsql = \
    """
        INSERT INTO nacional.o_token 
            (token, createat, updateat, userid) 
        VALUES(%(token)s, %(createat)s, %(updateat)s, %(userid)s)
    """
#vp2.enable = 1 and