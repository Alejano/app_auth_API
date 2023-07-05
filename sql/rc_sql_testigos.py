class SqlStrings():
    is_call_center =  \
    """
    SELECT * from redesc.get_escallcenter({},{});
    """
    
    ins_testigos_pgsql =  \
    """
    SELECT * from redesc.inserta_o_testigo({},'{}',{},{},{},'{}','{}','{}','{}','{}','{}','{}','{}',{},{},'{}',{},'{}',{});
    """

    update_testigos_pgsql =  \
    """
    UPDATE redesc.o_testigos SET img1='{}',img2='{}',img3='{}',img4='{}',img5='{}',img6='{}',img7='{}',img8='{}',img9='{}',img10='{}' where testigoid={} ;
    """

    get_CuentasTestigos =  \
    """
    SELECT redesc.recupera_registrost({});
    """
    
    get_Testigos =  \
    """
    SELECT * from redesc.get_testigos_search_pages({},{},{},{},{},{},{},{},'{}','{}');
    """
    get_Testigos_ref =  \
    """
    SELECT * from redesc.get_testigos_search_pages({},{},{},{},{},'{}',{},{},'{}','{}');
    """
    get_Testigos_user =  \
    """
    SELECT * from redesc.get_testigos_search_pages({},{},{},{},'{}',{},{},{},'{}','{}');
    """
    get_Testigos_usref =  \
    """
    SELECT * from redesc.get_testigos_search_pages({},{},{},{},'{}','{}',{},{},'{}','{}');
    """
    
    
    get_Count_Testigos =  \
    """
    SELECT count(*) from redesc.get_testigos_search_pages(10000000000,0,{},{},{},{},{},{},'{}','{}');
    """
    
    get_Testigos_null =  \
    """
    SELECT * from redesc.get_testigos_search_pages({},{},{},{},{},{},{},{},{},{});
    """
    get_Count_Testigos_null =  \
    """
    SELECT count(*) from redesc.get_testigos_search_pages(10000000000,0,{},{},{},{},{},{},{},{});
    """
    
    get_imagenTestigos =  \
    """
    SELECT img1,img2,img3,img4,img5,img6,img7,img8,img9,img10 FROM redesc.o_testigos where testigoid={};
    """

