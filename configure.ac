AC_PREREQ(2.52)

AC_INIT([apertium-quc], [0.1.0], [ftyers@prompsit.com])
AM_INIT_AUTOMAKE
AC_PROG_LN_S
AC_PROG_AWK

dnl HFST support
AH_TEMPLATE(HAVE_HFSTOSPELL, [Have HFSTOSPELL])
AC_ARG_ENABLE(ospell, AC_HELP_STRING([--enable-ospell],
        [enable HFST spellchecking backend]),
        [hfstospell=${enableval}], [hfstospell=no])
dnl must be AS_IF for some aclocals to pick PKG_CHECK_MODULES somehow.
dnl AC_PROVIDE_IFELSE doesn't work on mac?
AS_IF([test x$hfstospell = xyes], [
      PKG_CHECK_MODULES([HFSTOSPELL], [hfstospell >= 0.2])
          AC_DEFINE(HAVE_HFSTOSPELL, 1)
          CXXFLAGS="$CXXFLAGS $HFSTOSPELL_CFLAGS"
        ])
AM_CONDITIONAL([HAVE_HFSTOSPELL], [test x$hfstospell = xyes])


m4_define([required_apertium_version], [3.3.0])
PKG_CHECK_MODULES(APERTIUM,   apertium >= required_apertium_version)
PKG_CHECK_MODULES(HFST,       hfst >= 3.15.2)

AC_CHECK_PROG([HFSTLEXC], [hfst-lexc], [yes], [no])
AS_IF([test x$HFSTLEXC = xno], [AC_MSG_ERROR([You don't have hfst-lexc installed])])

AC_CHECK_PROG([HFSTTWOLC], [hfst-twolc], [yes], [no])
AS_IF([test x$HFSTTWOLC = xno], [AC_MSG_ERROR([You don't have hfst-twolc installed])])

AC_CHECK_PROG([HFSTREALIGN], [hfst-realign], [yes], [no])
AS_IF([test x$HFSTREALIGN = xno], [AC_MSG_ERROR([You don't have hfst-realign installed])])

AC_CHECK_PROG([CGCOMP], [cg-comp], [yes], [no])
AS_IF([test x$CGCOMP = xno], [AC_MSG_ERROR([You don't have cg-comp installed])])


AP_MKINCLUDE

AC_OUTPUT([Makefile apertium-quc.pc])
