" Summer's Configuration file for vim based on hongbo's share
" Email:summer@snakr.com
" Blog: http://summic.com

set modelines=0		" CVE-2007-2438

" Normally we use vim-extensions. If you want true vi-compatibility
" remove change the following statements
set nocompatible	" Use Vim defaults instead of 100% vi compatibility
set backspace=2		" more powerful backspacing

" Don't write backup file if vim is being called by "crontab -e"
au BufWrite /private/tmp/crontab.* set nowritebackup
" Don't write backup file if vim is being called by "chpass"
au BufWrite /private/etc/pw.* set nowritebackup

set nu
"编码设置
"utf-8编码
" 设置编码
set enc=utf-8
" 设置文件编码
set fenc=utf-8
" 设置文件编码检测类型及支持格式
set fencs=gbk,utf-8,ucs-bom,gb18030,gb2312,cp936
" 指定菜单语言
set langmenu=zh_CN.utf-8
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim 
language messages zh_CN.utf-8

set encoding=utf-8
set fileencodings=ucs-bom,utf8,chinese,taiwan,ansi
set guifont=Courier_New:h12:w7
set guifontwide=NSimSun-18030,NSimSun
set ambiwidth=double
set termencoding=utf-8
" 状态行颜色
highlight StatusLine guifg=SlateBlue guibg=Yellow
highlight StatusLineNC guifg=Gray guibg=White

" 不要备份文件（根据自己需要取舍）
set nobackup

" 命令行（在状态行下）的高度，默认为1，这里是2
set cmdheight=1

" 通过使用: commands命令，告诉我们文件的哪一行被改变过
set report=0

" 光标移动到buffer的顶部和底部时保持3行距离
set scrolloff=3

" 语法高亮
filetype plugin indent on
syntax enable

" 函数自动完成
"" 需要下载php函数列表 http://cvs.php.net/viewvc.cgi/phpdoc/funclist.txt?view=co
set dictionary-=/var/www/.vim/php.dict dictionary+=/var/www/.vim/php.dict

"Use the dictionary completion
set complete-=k complete+=k

function! InsertTabWrapper()
    let col=col('.')-1
    if !col || getline('.')[col-1] !~ '\k'
                return "\<TAB>"
                    else
    return "\<C-N>"
    endif
endfunction

"Remap the tab key to select action with InsertTabWrapper
inoremap <TAB> <C-R>=InsertTabWrapper()<CR>

"TAB缩进设置===============
set expandtab
"set sw=4
set et sw=4 ts=4 sts=4
set tabstop=4
set softtabstop=4
