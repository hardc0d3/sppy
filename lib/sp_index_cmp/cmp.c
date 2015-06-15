#include<stdio.h>
#include<string.h>
#include<inttypes.h>

#define srlikely(EXPR)   __builtin_expect(!! (EXPR), 1)
#define srunlikely(EXPR) __builtin_expect(!! (EXPR), 0)


extern int
compare_function(char *a, size_t asz, char *b, size_t bsz, void *arg)
{
   return 0;
}

/* mot mo copy pasted from
sophia/sophia/rt/sr_cmp.c
*/

extern int 
compare_str(char *a, size_t asz, char *b, size_t bsz, void *arg)
{
        register int size = (asz < bsz) ? asz : bsz;

        register int rc = memcmp(a, b, size);
        if (srunlikely(rc == 0)) {
                if (srlikely(asz == bsz))
                        return 0;
                return (asz < bsz) ? -1 : 1;
        }
        return rc > 0 ? 1 : -1;
}  


extern int
compare_u32list(char *a, size_t asz, char *b, size_t bsz, void *arg)
{

register int bufsz  = ( asz < bsz ) ? asz : bsz;
register uint32_t ua;
register uint32_t ub;
register int i;

a+=4;
b+=4;

for ( i = 4; i<bufsz; i+=4 ) {

     ua = *(uint32_t*) a;
     ub = *(uint32_t*) b;

       if( ua < ub) { return -1; }
       else if ( ua > ub ) { return 1; }
       //else { return 0; }
       a+=4;
       b+=4;
       
  }
  printf ("asz %d bsz %d bufsz %d", asz,bsz,bufsz );
  if( asz < bsz ) { return -1;}
  else if ( asz > bsz ) { return 1; }
  else { return 0; }

  return 0;

}

extern int 
print_pointer ( char* pointer, size_t psz, void* func) {
    return snprintf(pointer, psz, "pointer: %p", (void*)func);    
  } 

    



