#!/usr/bin/env python3
#  Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from nose2.tools import params

from fruit_test_common import *

COMMON_DEFINITIONS = '''
#include <fruit/fruit.h>
#include <vector>
#include "test_macros.h"

struct Annotation1 {};
struct Annotation2 {};
struct Annotation3 {};
'''

def test_success_copyable_and_movable():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
  X(X&&) = default;
  X(const X&) = default;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent();
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

# TODO: move to test_register_provider.py
def test_success_copyable_and_movable_provider_returning_value():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = default;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerProvider([](){return X();});
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

# TODO: move to test_register_provider.py
def test_success_copyable_and_movable_provider_returning_pointer():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = default;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerProvider([](){return new X();});
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

def test_success_movable_only():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
  X(X&&) = default;
  X(const X&) = delete;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent();
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

# TODO: move to test_register_provider.py
def test_success_movable_only_provider_returning_value():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = delete;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerProvider([](){return X();});
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

# TODO: move to test_register_provider.py
def test_success_movable_only_provider_returning_pointer():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = delete;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerProvider([](){return new X();});
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

def test_success_not_movable():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
  X(X&&) = delete;
  X(const X&) = delete;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent();
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

# TODO: move to test_register_provider.py
def test_success_not_movable_provider_returning_pointer():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = delete;
  X(const X&) = delete;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerProvider([](){return new X();});
}

int main() {
  fruit::Injector<X> injector(getComponent());
  injector.get<X*>();
}
''')

# TODO: move to test_register_factory.py
@params('std::function<X()>', 'fruit::Annotated<Annotation1, std::function<X()>>')
def test_success_factory_copyable_and_movable_implicit(XFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
  X(X&&) = default;
  X(const X&) = default;
};

fruit::Component<XFactoryAnnot> getComponent() {
  return fruit::createComponent();
}

int main() {
  fruit::Injector<XFactoryAnnot> injector(getComponent());
  injector.get<XFactoryAnnot>()();
}
''',
    locals())

# TODO: move to test_register_factory.py
@params(
    ('X', 'std::function<X()>'),
    ('fruit::Annotated<Annotation1, X>', 'fruit::Annotated<Annotation1, std::function<X()>>'))
def test_success_factory_copyable_and_movable_explicit_returning_value(XAnnot, XFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = default;
};

fruit::Component<XFactoryAnnot> getComponent() {
  return fruit::createComponent()
    .registerFactory<XAnnot()>([](){return X();});
}

int main() {
  fruit::Injector<XFactoryAnnot> injector(getComponent());
  injector.get<XFactoryAnnot>()();
}
''',
    locals())

# TODO: move to test_register_factory.py
@params(
    ('X', 'std::unique_ptr<X>', 'std::function<std::unique_ptr<X>()>'),
    ('fruit::Annotated<Annotation1, X>', 'fruit::Annotated<Annotation1, std::unique_ptr<X>>', 'fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>'))
def test_success_factory_copyable_and_movable_explicit_returning_pointer(XAnnot, XPtrAnnot, XPtrFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = default;
};

fruit::Component<XPtrFactoryAnnot> getComponent() {
  return fruit::createComponent()
    .registerFactory<XPtrAnnot()>([](){return std::unique_ptr<X>();});
}

int main() {
  fruit::Injector<XPtrFactoryAnnot> injector(getComponent());
  injector.get<XPtrFactoryAnnot>()();
}
''',
    locals())

# TODO: move to test_register_factory.py
@params('std::function<X()>', 'fruit::Annotated<Annotation1, std::function<X()>>')
def test_success_factory_movable_only_implicit(XFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
  X(X&&) = default;
  X(const X&) = delete;
};

fruit::Component<XFactoryAnnot> getComponent() {
  return fruit::createComponent();
}

int main() {
  fruit::Injector<XFactoryAnnot> injector(getComponent());
  injector.get<XFactoryAnnot>()();
}
''',
    locals())

# TODO: move to test_register_factory.py
@params(
    ('X', 'std::function<X()>'),
    ('fruit::Annotated<Annotation1, X>', 'fruit::Annotated<Annotation1, std::function<X()>>'))
def test_success_factory_movable_only_explicit_returning_value(XAnnot, XFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = delete;
};

fruit::Component<XFactoryAnnot> getComponent() {
  return fruit::createComponent()
    .registerFactory<XAnnot()>([](){return X();});
}

int main() {
  fruit::Injector<XFactoryAnnot> injector(getComponent());
  injector.get<XFactoryAnnot>()();
}
''',
    locals())

# TODO: move to test_register_factory.py
@params(
    ('X', 'std::unique_ptr<X>', 'std::function<std::unique_ptr<X>()>'),
    ('fruit::Annotated<Annotation1, X>', 'fruit::Annotated<Annotation1, std::unique_ptr<X>>', 'fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>'))
def test_success_factory_movable_only_explicit_returning_pointer(XAnnot, XPtrAnnot, XPtrFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = default;
  X(const X&) = delete;
};

fruit::Component<XPtrFactoryAnnot> getComponent() {
  return fruit::createComponent()
    .registerFactory<XPtrAnnot()>([](){return std::unique_ptr<X>();});
}

int main() {
  fruit::Injector<XPtrFactoryAnnot> injector(getComponent());
  injector.get<XPtrFactoryAnnot>()();
}
''',
    locals())

# TODO: move to test_register_factory.py
@params('std::function<std::unique_ptr<X>()>', 'fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>')
def test_success_factory_not_movable_implicit(XPtrFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
  X(X&&) = delete;
  X(const X&) = delete;
};

fruit::Component<XPtrFactoryAnnot> getComponent() {
  return fruit::createComponent();
}

int main() {
  fruit::Injector<XPtrFactoryAnnot> injector(getComponent());
  injector.get<XPtrFactoryAnnot>()();
}
''',
    locals())

# TODO: move to test_register_factory.py
@params(
    ('std::unique_ptr<X>', 'std::function<std::unique_ptr<X>()>'),
    ('fruit::Annotated<Annotation1, std::unique_ptr<X>>', 'fruit::Annotated<Annotation1, std::function<std::unique_ptr<X>()>>'))
def test_success_factory_not_movable_explicit_returning_pointer_with_annotation(XPtrAnnot, XPtrFactoryAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  X() = default;
  X(X&&) = delete;
  X(const X&) = delete;
};

fruit::Component<XPtrFactoryAnnot> getComponent() {
  return fruit::createComponent()
    .registerFactory<XPtrAnnot()>([](){return std::unique_ptr<X>();});
}

int main() {
  fruit::Injector<XPtrFactoryAnnot> injector(getComponent());
  injector.get<XPtrFactoryAnnot>()();
}
''',
    locals())


# TODO: consider moving to test_normalized_component.py
@params(
    ('X', 'Y', 'Z'),
    ('fruit::Annotated<Annotation1, X>', 'fruit::Annotated<Annotation2, Y>', 'fruit::Annotated<Annotation3, Z>'),)
def test_autoinject_with_annotation_success(XAnnot, YAnnot, ZAnnot):
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  using Inject = X();
};

struct Y {
  using Inject = Y();
  Y() {
    Assert(!constructed);
    constructed = true;
  }

  static bool constructed;
};

bool Y::constructed = false;

struct Z {
  using Inject = Z();
};

fruit::Component<ZAnnot, YAnnot, XAnnot> getComponent() {
  return fruit::createComponent();
}

int main() {
  fruit::NormalizedComponent<> normalizedComponent(fruit::createComponent());
  fruit::Injector<YAnnot> injector(normalizedComponent, getComponent());

  Assert(!Y::constructed);
  injector.get<YAnnot>();
  Assert(Y::constructed);
}
''',
    locals())

def test_autoinject_annotation_in_signature_return_type():
    expect_compile_error(
    'InjectTypedefWithAnnotationError<X>',
    'C::Inject is a signature that returns an annotated type',
    COMMON_DEFINITIONS + '''
struct X;
using XAnnot = fruit::Annotated<Annotation1, X>;

struct X {
  using Inject = XAnnot();
};

fruit::Component<XAnnot> getComponent() {
  return fruit::createComponent();
}
''')

def test_autoinject_wrong_class_in_typedef():
    expect_compile_error(
    'InjectTypedefForWrongClassError<Y,X>',
    'C::Inject is a signature, but does not return a C. Maybe the class C has no Inject typedef and',
    COMMON_DEFINITIONS + '''
struct X {
  using Inject = X();
};

struct Y : public X {
};

fruit::Component<Y> getComponent() {
  return fruit::createComponent();
}
''')

def test_error_abstract_class():
    expect_compile_error(
    'CannotConstructAbstractClassError<X>',
    'The specified class can.t be constructed because it.s an abstract class.',
    COMMON_DEFINITIONS + '''
struct X {
  X(int*) {}

  virtual void foo() = 0;
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerConstructor<fruit::Annotated<Annotation1, X>(int*)>();
}
''')

def test_error_malformed_signature():
    expect_compile_error(
    'NotASignatureError<X\[\]>',
    'CandidateSignature was specified as parameter, but it.s not a signature. Signatures are of the form',
    COMMON_DEFINITIONS + '''
struct X {
  X(int) {}
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerConstructor<X[]>();
}
''')

def test_error_malformed_signature_autoinject():
    expect_compile_error(
    'InjectTypedefNotASignatureError<X,X\[\]>',
    'C::Inject should be a typedef to a signature',
    COMMON_DEFINITIONS + '''
struct X {
  using Inject = X[];
  X(int) {}
};

fruit::Component<X> getComponent() {
  return fruit::createComponent();
}
''')

@params('char*', 'fruit::Annotated<Annotation1, char*>')
def test_error_does_not_exist(charPtrAnnot):
    expect_compile_error(
    'NoConstructorMatchingInjectSignatureError<X,X\(char\*\)>',
    'contains an Inject typedef but it.s not constructible with the specified types',
    COMMON_DEFINITIONS + '''
struct X {
  X(int*) {}
};

fruit::Component<X> getComponent() {
  return fruit::createComponent()
    .registerConstructor<X(charPtrAnnot)>();
}
''',
    locals())

@params('char*', 'fruit::Annotated<Annotation1, char*>')
def test_error_does_not_exist_autoinject(charPtrAnnot):
    expect_compile_error(
    'NoConstructorMatchingInjectSignatureError<X,X\(char\*\)>',
    'contains an Inject typedef but it.s not constructible with the specified types',
    COMMON_DEFINITIONS + '''
struct X {
  using Inject = X(charPtrAnnot);
  X(int*) {}
};

fruit::Component<X> getComponent() {
  return fruit::createComponent();
}
''',
    locals())

def test_error_abstract_class_autoinject():
    expect_compile_error(
    'CannotConstructAbstractClassError<X>',
    'The specified class can.t be constructed because it.s an abstract class.',
    COMMON_DEFINITIONS + '''
struct X {
  using Inject = fruit::Annotated<Annotation1, X>();

  virtual void scale() = 0;
  // Note: here we "forgot" to implement scale() (on purpose, for this test) so X is an abstract class.
};

fruit::Component<fruit::Annotated<Annotation1, X>> getComponent() {
  return fruit::createComponent();
}
''')

if __name__ == '__main__':
    import nose2
    nose2.main()
