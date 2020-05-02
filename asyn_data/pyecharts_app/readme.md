问题1：把<script>中的部分代码放在head中无法加载出来
    Preview:
    HTML的加载和渲染：
         JS代码可能会改变DOM树结构，导致浏览器需要重新构建DOM树，so 要是加载嵌入式JS的话，浏览器会阻塞其内容的下载和呈现
    window.onload和$().ready(function)的区别     
        window.onload是在dom文档树加载完和所有文件加载完之后执行
        jquery中有$().ready(function),在dom文档树加载完之后执行一个函数（注意，这里面的文档树加载完全不代表全部文件加载完）

        $(document).ready要比winndow.onload先执行

        window.onload只能出来一次，$(document).ready可以出现多次
        
        答：JS代码中的$(document).ready(function () {} 是在DOM树结构加载完毕后就执行，
        此时Pyechart 需要的图片之类的资源还没有加载完毕，所以将其放在head中呆滞程序无法跑通



