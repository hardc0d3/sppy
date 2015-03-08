#include<stdio.h>
#include<string.h>


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
print_pointer ( char* pointer, size_t psz, void* func) {
    return snprintf(pointer, psz, "pointer: %p", (void*)func);    
  } 

    



